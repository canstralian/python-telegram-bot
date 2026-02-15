#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2023
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""This module contains an object that represents a Encrypted PassportFile."""

from typing import TYPE_CHECKING, List, Optional, Tuple

from telegram._telegramobject import TelegramObject
from telegram._utils.defaultvalue import DEFAULT_NONE
from telegram._utils.types import JSONDict, ODVInput

if TYPE_CHECKING:
    from telegram import Bot, File, FileCredentials


class PassportFile(TelegramObject):
    """
    This object represents a file uploaded to Telegram Passport. Currently all Telegram Passport
    files are in JPEG format when decrypted and don't exceed 10MB.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`file_unique_id` is equal.

    Args:
        file_id (:obj:`str`): Identifier for this file, which can be used to download
            or reuse the file.
        file_unique_id (:obj:`str`): Unique identifier for this file, which
            is supposed to be the same over time and for different bots.
            Can't be used to download or reuse the file.
        file_size (:obj:`int`): File size in bytes.
        file_date (:obj:`int`): Unix time when the file was uploaded.

    Attributes:
        file_id (:obj:`str`): Identifier for this file, which can be used to download
            or reuse the file.
        file_unique_id (:obj:`str`): Unique identifier for this file, which
            is supposed to be the same over time and for different bots.
            Can't be used to download or reuse the file.
        file_size (:obj:`int`): File size in bytes.
        file_date (:obj:`int`): Unix time when the file was uploaded.


    """

    __slots__ = (
        "file_date",
        "file_id",
        "file_size",
        "_credentials",
        "file_unique_id",
    )

    def __init__(
        self,
        file_id: str,
        file_unique_id: str,
        file_date: int,
        file_size: int,
        credentials: Optional["FileCredentials"] = None,
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(api_kwargs=api_kwargs)

        # Required
        self.file_id: str = file_id
        self.file_unique_id: str = file_unique_id
        self.file_size: int = file_size
        self.file_date: int = file_date
        # Optionals

        self._credentials: Optional[FileCredentials] = credentials

        self._id_attrs = (self.file_unique_id,)

        self._freeze()

    @classmethod
    def de_json_decrypted(
        cls, data: Optional[JSONDict], bot: "Bot", credentials: "FileCredentials"
    ) -> Optional["PassportFile"]:
        """Variant of :meth:`telegram.TelegramObject.de_json` that also takes into account
        passport credentials.

        Args:
            data (Dict[:obj:`str`, ...]): The JSON data.
            bot (:class:`telegram.Bot`): The bot associated with this object.
            credentials (:class:`telegram.FileCredentials`): The credentials

        Returns:
            :class:`telegram.PassportFile`:
        
        Raises:
            :class:`ValueError`: If data is malformed or credentials are invalid

        """
        data = cls._parse_data(data)

        if not data:
            return None
        
        # Validate credentials before proceeding
        if credentials is None:
            raise ValueError("FileCredentials cannot be None for decrypted PassportFile")

        data["credentials"] = credentials

        return super().de_json(data=data, bot=bot)

    @classmethod
    def de_list_decrypted(
        cls, data: Optional[List[JSONDict]], bot: "Bot", credentials: List["FileCredentials"]
    ) -> Tuple[Optional["PassportFile"], ...]:
        """Variant of :meth:`telegram.TelegramObject.de_list` that also takes into account
        passport credentials.

        .. versionchanged:: 20.0

           * Returns a tuple instead of a list.
           * Filters out any :obj:`None` values

        Args:
            data (List[Dict[:obj:`str`, ...]]): The JSON data.
            bot (:class:`telegram.Bot`): The bot associated with these objects.
            credentials (:class:`telegram.FileCredentials`): The credentials

        Returns:
            Tuple[:class:`telegram.PassportFile`]:

        """
        if not data:
            return ()

        return tuple(
            obj
            for obj in (
                cls.de_json_decrypted(passport_file, bot, credentials[i])
                for i, passport_file in enumerate(data)
            )
            if obj is not None
        )

    async def get_file(
        self,
        *,
        read_timeout: ODVInput[float] = DEFAULT_NONE,
        write_timeout: ODVInput[float] = DEFAULT_NONE,
        connect_timeout: ODVInput[float] = DEFAULT_NONE,
        pool_timeout: ODVInput[float] = DEFAULT_NONE,
        api_kwargs: Optional[JSONDict] = None,
    ) -> "File":
        """
        Wrapper over :meth:`telegram.Bot.get_file`. Will automatically assign the correct
        credentials to the returned :class:`telegram.File` if originating from
        :obj:`telegram.PassportData.decrypted_data`.

        For the documentation of the arguments, please see :meth:`telegram.Bot.get_file`.

        Returns:
            :class:`telegram.File`

        Raises:
            :class:`telegram.error.TelegramError`
            :class:`ValueError`: If file_id is invalid or bot is not set

        """
        # Validate file_id before making the request
        if not self.file_id or not isinstance(self.file_id, str):
            raise ValueError("Invalid file_id: must be a non-empty string")
        
        # Validate that bot is available
        bot = self.get_bot()
        if bot is None:
            raise ValueError("Bot instance is not set. Cannot retrieve file.")
        
        try:
            file = await bot.get_file(
                file_id=self.file_id,
                read_timeout=read_timeout,
                write_timeout=write_timeout,
                connect_timeout=connect_timeout,
                pool_timeout=pool_timeout,
                api_kwargs=api_kwargs,
            )
            file.set_credentials(self._credentials)
            return file
        except Exception as exc:
            # Re-raise with more context
            raise type(exc)(
                f"Failed to retrieve PassportFile with file_id '{self.file_id}': {exc}"
            ) from exc

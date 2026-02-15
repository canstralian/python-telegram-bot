.. image:: https://raw.githubusercontent.com/python-telegram-bot/logos/master/logo-text/png/ptb-logo-text_768.png
:align: center
:target: https://python-telegram-bot.org
:alt: python-telegram-bot Logo
.. image:: https://img.shields.io/pypi/v/python-telegram-bot.svg
:target: https://pypi.org/project/python-telegram-bot/
.. image:: https://img.shields.io/badge/Bot%20API-6.7-blue?logo=telegram
:target: https://core.telegram.org/bots/api-changelog
.. image:: https://img.shields.io/pypi/l/python-telegram-bot.svg
:target: https://www.gnu.org/licenses/lgpl-3.0.html
.. image:: https://codecov.io/gh/python-telegram-bot/python-telegram-bot/branch/master/graph/badge.svg
:target: https://app.codecov.io/gh/python-telegram-bot/python-telegram-bot
.. image:: https://app.deepsource.com/gh/python-telegram-bot/python-telegram-bot.svg/?label=active+issues
:target: https://app.deepsource.com/gh/python-telegram-bot/python-telegram-bot/
The wrapper you can't refuse—built for robust, asynchronous automation.
Introduction
This library provides a pure Python, asynchronous interface for the Telegram Bot API <https://core.telegram.org/bots/api>_. Engineered for Python 3.8+, it supports high-level abstractions via telegram.ext to accelerate the Implementation phase of your SDLC.
Purple Team & Security Focus
As a collaborator in offensive and defensive security, use this library to bridge the gap:
 * Offensive: Build C2 (Command & Control) interfaces or exfiltration notification bots.
 * Defensive: Create real-time alerting systems for SOC environments.
 * SDLC Integration: Ensure your bot moves through a structured pipeline:
   * Design: Utilize telegram.ext for modular, scalable bot architecture.
   * Testing: Leverage the built-in asyncio support to write robust unit tests.
   * Maintenance: Use GPG-verified releases to ensure supply chain integrity.
Verifying Integrity
In a purple team context, trust is earned. We sign all releases with a GPG key to prevent MITM or supply chain injections.
Find the public keys here <https://github.com/python-telegram-bot/python-telegram-bot/tree/master/public_keys>_.
Installation
Standard deployment:
.. code:: shell
$ pip install python-telegram-bot --upgrade

For specialized environments (e.g., routing through a proxy for OpSec):
.. code:: shell
$ pip install "python-telegram-bot[socks]"

Quick Start: The "Echo" Baseline
The Implementation stage usually begins with a functional baseline. View the echobot.py in our examples section <https://docs.python-telegram-bot.org/examples.html>_ to see the asynchronous dispatcher in action.
Technical Resources
 * Technical Documentation <https://docs.python-telegram-bot.org/>_ (API Reference)
 * Project Wiki <https://github.com/python-telegram-bot/python-telegram-bot/wiki/>_ (Deep Dives)
 * Official Telegram API <https://core.telegram.org/bots/api>_ (The source of truth)
Concurrency & Risk
Since v20.0, PTB is built on asyncio. Note that it is not thread-safe. In your Design phase, account for potential race conditions if using multi-threaded logging or database wrappers alongside the Application builder.
License
Licensed under LGPL-3. Build, modify, and secure freely.
Would you like me to generate a secure boilerplate Python script for a Telegram C2 bot using this library?


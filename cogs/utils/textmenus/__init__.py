# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2015-2019 Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import asyncio
import discord
import inspect
import logging
import traceback
import datetime
from collections import OrderedDict

log = logging.getLogger(__name__)

class MenuError(Exception):
    pass


class CannotEmbedLinks(MenuError):
    def __init__(self):
        super().__init__('Bot does not have embed links permission in this channel.')


class CannotSendMessages(MenuError):
    def __init__(self):
        super().__init__('Bot cannot send messages in this channel.')


class CannotAddReactions(MenuError):
    def __init__(self):
        super().__init__('Bot cannot add reactions in this channel.')


class CannotReadMessageHistory(MenuError):
    def __init__(self):
        super().__init__('Bot does not have Read Message History permissions in this channel.')


class ExitException(Exception):
    pass


class StopException(Exception):
    pass


def should_stop_or_exit(payload):
    if payload.content.lower() == 'stop':
        raise StopException
    if payload.content.lower() == 'exit':
        raise ExitException


def get_menu_exit_reason(menu):
    if isinstance(menu.exception, ExitException):
        return "'exit' received."
    if isinstance(menu.exception, StopException):
        return "'stop' received."
    if menu.timed_out:
        return "Menu timed out."
    return ""


class EmbedInfo:
    class Field:
        def __init__(self, name, value, inline=False):
            self.name = name
            self.value = value
            self.inline = inline
    class Author:
        def __init__(self, name, url, icon_url):
            self.name = name
            self.url = url
            self.icon_url = icon_url

    def __init__(self, thumbnail, author, colour, footer_text, fields):
        self.thumbnail = thumbnail
        self.author = author
        self.colour = colour
        self.footer_text = footer_text
        self.fields = fields

    def convert_empty_fields(self):
        """
        Helper function if needed. Probably shouldn't be used.
        :return:
        """
        fields = []
        for f in [f for f in self.fields if f]:
            if not f.name:
                f.name = '\u200b'
            if not f.value:
                f.value = '\u200b'
            fields.append(f)
        self.fields = fields



class Position:
    __slots__ = ('number', 'bucket')

    def __init__(self, number, *, bucket=1):
        self.bucket = bucket
        self.number = number

    def __lt__(self, other):
        if not isinstance(other, Position) or not isinstance(self, Position):
            return NotImplemented

        return (self.bucket, self.number) < (other.bucket, other.number)

    def __eq__(self, other):
        return isinstance(other, Position) and other.bucket == self.bucket and other.number == self.number

    def __le__(self, other):
        r = Position.__lt__(other, self)
        if r is NotImplemented:
            return NotImplemented
        return not r

    def __gt__(self, other):
        return Position.__lt__(other, self)

    def __ge__(self, other):
        r = Position.__lt__(self, other)
        if r is NotImplemented:
            return NotImplemented
        return not r

    def __repr__(self):
        return '<{0.__class__.__name__}: {0.number}>'.format(self)


class Last(Position):
    __slots__ = ()

    def __init__(self, number=0):
        super().__init__(number, bucket=2)


class First(Position):
    __slots__ = ()

    def __init__(self, number=0):
        super().__init__(number, bucket=0)


class Submenu:
    """Represents a reaction-style button for the :class:`Menu`.

    There are two ways to create this, the first being through explicitly
    creating this class and the second being through the decorator interface,
    :func:`button`.

    The action must have both a ``self`` and a ``payload`` parameter
    of type :class:`discord.RawReactionActionEvent`.

    Attributes
    ------------
    label: :class:`str`
        The label to use
    action
        A coroutine that is called when the button is pressed.
    skip_if: Optional[Callable[[:class:`Menu`], :class:`bool`]]
        A callable that detects whether it should be skipped.
        A skipped button does not show up in the reaction list
        and will not be processed.
    position: :class:`Position`
        The position the button should have in the initial order.
        Note that since Discord does not actually maintain reaction
        order, this is a best effort attempt to have an order until
        the user restarts their client. Defaults to ``Position(0)``.
    lock: :class:`bool`
        Whether the button should lock all other buttons from being processed
        until this button is done. Defaults to ``True``.
    """
    __slots__ = ('label', '_action', '_skip_if', 'position', 'lock')

    def __init__(self, label, action, *, skip_if=None, position=None, lock=True):
        self.label = label
        self.action = action
        self.skip_if = skip_if
        self.position = position or Position(0)
        self.lock = lock

    @property
    def skip_if(self):
        return self._skip_if

    @skip_if.setter
    def skip_if(self, value):
        if value is None:
            self._skip_if = lambda x: False
            return

        try:
            menu_self = value.__self__
        except AttributeError:
            self._skip_if = value
        else:
            # Unfurl the method to not be bound
            if not isinstance(menu_self, Menu):
                raise TypeError('skip_if bound method must be from Menu not %r' % menu_self)

            self._skip_if = value.__func__

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        try:
            menu_self = value.__self__
        except AttributeError:
            pass
        else:
            # Unfurl the method to not be bound
            if not isinstance(menu_self, Menu):
                raise TypeError('action bound method must be from Menu not %r' % menu_self)

            value = value.__func__

        if not inspect.iscoroutinefunction(value):
            raise TypeError('action must be a coroutine not %r' % value)

        self._action = value

    def __call__(self, menu, payload):
        if self.skip_if(menu):
            return
        return self._action(menu, payload)

    def __str__(self):
        return str(self.label)

    def is_valid(self, menu):
        return not self.skip_if(menu)


def submenu(label, **kwargs):
    """Denotes a method to be submenu for the :class:`Menu`.

    The methods being wrapped must have both a ``self`` and a ``payload``
    parameter of type :class:`discord.RawReactionActionEvent`.

    The keyword arguments are forwarded to the :class:`Submenu` constructor.

    Example
    ---------

    .. code-block:: python3

        class MyMenu(Menu):
            async def send_initial_message(self, ctx, channel):
                return await channel.send(f'Hello {ctx.author}')

            @button('\\N{THUMBS UP SIGN}')
            async def on_thumbs_up(self, payload):
                await self.message.edit(content=f'Thanks {self.ctx.author}!')

            @button('\\N{THUMBS DOWN SIGN}')
            async def on_thumbs_down(self, payload):
                await self.message.edit(content=f"That's not nice {self.ctx.author}...")

    Parameters
    ------------
    emoji: Union[:class:`str`, :class:`discord.PartialEmoji`]
        The emoji to use for the button.
    """

    def decorator(func):
        func._menu_label__ = label
        func.__menu_label_kwargs__ = kwargs
        return func

    return decorator


class _MenuMeta(type):
    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # This is needed to maintain member order for the submenus
        return OrderedDict()

    def __new__(cls, name, bases, attrs, **kwargs):
        submenus = []
        new_cls = super().__new__(cls, name, bases, attrs)

        inherit_submenus = kwargs.pop('inherit_submenus', True)
        if inherit_submenus:
            # walk MRO to get all submenus even in subclasses
            for base in reversed(new_cls.__mro__):
                for elem, value in base.__dict__.items():
                    try:
                        value._menu_label__
                    except AttributeError:
                        continue
                    else:
                        submenus.append(value)
        else:
            for elem, value in attrs.items():
                try:
                    value._menu_label__
                except AttributeError:
                    continue
                else:
                    submenus.append(value)

        new_cls.__menu_labels__ = submenus
        return new_cls

    def get_submenus(cls):
        submenus = OrderedDict()
        for func in cls.__menu_labels__:
            label = func._menu_label__
            submenus[label] = Submenu(label, func, **func.__menu_label_kwargs__)
        return submenus


class Menu(metaclass=_MenuMeta):
    r"""An interface that allows handling menus by using reactions as buttons.

    Buttons should be marked with the :func:`button` decorator. Please note that
    this expects the methods to have a single parameter, the ``payload``. This
    ``payload`` is of type :class:`discord.RawReactionActionEvent`.

    Attributes
    ------------
    timeout: :class:`float`
        The timeout to wait between button inputs.
    delete_message_after: :class:`bool`
        Whether to delete the message after the menu interaction is done.
    check_embeds: :class:`bool`
        Whether to verify embed permissions as well.
    ctx: Optional[:class:`commands.Context`]
        The context that started this pagination session or ``None`` if it hasn't
        been started yet.
    bot: Optional[:class:`commands.Bot`]
        The bot that is running this pagination session or ``None`` if it hasn't
        been started yet.
    message: Optional[:class:`discord.Message`]
        The message that has been sent for handling the menu. This is the returned
        message of :meth:`send_initial_message`. You can set it in order to avoid
        calling :meth:`send_initial_message`\, if for example you have a pre-existing
        message you want to attach a menu to.
    """

    def __init__(self, *, timeout=180.0,
                 # delete_message_after=False,
                 check_embeds=False,
                 message=None,
                 enumerate_submenus=True,
                 stop_on_first=True,
                 embed_info=None):
        log.debug(f"Menu::__init__ - {self.get_title()}")
        self.timeout = timeout
        # self.delete_message_after = delete_message_after
        self.check_embeds = check_embeds
        self.message = message
        self.enumerate_submenus = enumerate_submenus
        self.stop_on_first = stop_on_first
        self._can_remove_reactions = False
        self.__tasks = []
        self._running = True
        self.ctx = None
        self.bot = None
        self._author_id = None
        self._submenus = self.__class__.get_submenus()
        self._lock = asyncio.Lock()
        self._event = asyncio.Event()
        self._exception = None
        self.embed_info = embed_info
        self.channel = None
        if self.enumerate_submenus:
            self._enumerated_submenus = {str(i): key for i, key in enumerate(self.submenus.keys(), start=1)}

    @discord.utils.cached_property
    def submenus(self):
        """Retrieves the submenus that are to be used for this menu session.

        Skipped submenus are not in the resulting dictionary.

        Returns
        ---------
        Mapping[:class:`str`, :class:`Button`]
            A mapping of button emoji to the actual button class.
        """
        submenus = sorted(self._submenus.values(), key=lambda b: b.position)
        return {
            submenu.label: submenu
            for submenu in submenus
            if submenu.is_valid(self)
        }

    @discord.utils.cached_property
    def enumerated_submenus(self):
        return {str(i): key for i, key in enumerate(self.submenus.keys(), start=1)}

    def should_add_submenus(self):
        """:class:`bool`: Whether to add submenus to this menu session."""
        return len(self.submenus)

    def _verify_permissions(self, ctx, channel, permissions):
        if not permissions.send_messages:
            raise CannotSendMessages()

        if not permissions.read_message_history:
            raise CannotReadMessageHistory()

        if self.check_embeds and not permissions.embed_links:
            raise CannotEmbedLinks()

    def message_check(self, message):
        if message.channel != self.channel:
            return False
        if message.author.id != self._author_id:
            return False
        if message.content.lower() == 'stop':
            return True
        if message.content.lower() == 'exit':
            return True
        return message.content in self.enumerated_submenus if self.enumerate_submenus else self.submenus

    async def wait_for_reply(self):
        tasks = [
            asyncio.ensure_future(self.bot.wait_for('message', check=self.message_check)),
        ]
        done, pending = await asyncio.wait(tasks, timeout=self.timeout, return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()

        if len(done) == 0:
            raise asyncio.TimeoutError()

        # Exception will propagate if e.g. cancelled or timed out
        return done.pop().result()

    async def _internal_loop(self):
        try:
            self.__timed_out = False
            loop = self.bot.loop
            # Ensure the name exists for the cancellation handling
            tasks = []
            run_flag = True
            while self._running and run_flag:
                # if self.send_to_author
                await self.send_initial_message(self.ctx, self.channel)

                payload = await self.wait_for_reply()

                should_stop_or_exit(payload)

                # loop.create_task(self.update(payload))
                await self.update(payload)

                # Set run flag to false if we want to stop on first (useful for single text menu)
                if self.stop_on_first:
                    run_flag = False

                # NOTE: Removing the reaction ourselves after it's been done when
                # mixed with the checks above is incredibly racy.
                # There is no guarantee when the MESSAGE_REACTION_REMOVE event will
                # be called, and chances are when it does happen it'll always be
                # after the remove_reaction HTTP call has returned back to the caller
                # which means that the stuff above will catch the reaction that we
                # just removed.

                # For the future sake of myself and to save myself the hours in the future
                # consider this my warning.

        except asyncio.TimeoutError as err:
            self.__timed_out = True
            self._exception = err
        except ExitException as err:
            self._exception = err
        except StopException as err:
            self._exception = err
        except Exception as err:
            self._exception = err
            log.exception(err)
        finally:
            self._event.set()

            # Cancel any outstanding tasks (if any)
            for task in tasks:
                task.cancel()

            try:
                await self.finalize(self.__timed_out)
            except Exception:
                pass
            finally:
                self.__timed_out = False

            # Can't do any requests if the bot is closed
            if self.bot.is_closed():
                return

            # # Wrap it in another block anyway just to ensure
            # # nothing leaks out during clean-up
            # try:
            #     if self.delete_message_after:
            #         return await self.message.delete()
            # except Exception:
            #     logging.exception(f"{traceback.print_exc()}")

    async def update(self, payload):
        """|coro|

        Updates the menu after an event has been received.

        Parameters
        -----------
        payload: :class:`discord.RawReactionActionEvent`
            The reaction event that triggered this update.
        """
        if self.enumerate_submenus:
            key = self.enumerated_submenus[payload.content]
        else:
            key = payload.content

        submenu = self.submenus[key]

        if (self._running is False) and (self.stop_on_first is False):
            return

        try:
            if submenu.lock:
                async with self._lock:
                    if self._running or self.stop_on_first:
                        await submenu(self, payload)
            else:
                await submenu(self, payload)
        except ExitException as err:
            self._exception = err
        except StopException as err:
            # pass a stop exception to unwind back up to last looping menu
            self._exception = err
        except asyncio.TimeoutError as err:
            self._exception = err
        except Exception as err:
            # TODO: logging?
            self._exception = err
            log.debug(traceback.print_exc())
            log.exception(err)

    async def start(self, ctx, *, channel=None, wait=False, author=None):
        """|coro|

        Starts the interactive menu session.

        Parameters
        -----------
        ctx: :class:`Context`
            The invocation context to use.
        channel: :class:`discord.abc.Messageable`
            The messageable to send the message to. If not given
            then it defaults to the channel in the context.
        wait: :class:`bool`
            Whether to wait until the menu is completed before
            returning back to the caller.

        Raises
        -------
        MenuError
            An error happened when verifying permissions.
        discord.HTTPException
            Adding a reaction failed.
        """
        log.debug(f"Menu::start - {self.get_title()} - enter")
        # Clear the buttons cache and re-compute if possible.
        try:
            del self.submenus
            del self.enumerated_submenus
        except AttributeError:
            pass

        self.bot = bot = ctx.bot
        self.ctx = ctx
        self._author_id = author.id or ctx.author.id

        self.channel = channel or ctx.channel
        is_guild = isinstance(channel, discord.abc.GuildChannel)
        me = ctx.guild.me if is_guild else ctx.bot.user
        permissions = channel.permissions_for(me)
        self.__me = discord.Object(id=me.id)
        self._verify_permissions(ctx, channel, permissions)
        self._event.clear()

        # msg = self.message
        # if msg is None:
        #     self.message = msg = await self.send_initial_message(self.ctx, self.ctx.channel)

        for task in self.__tasks:
            task.cancel()
        self.__tasks.clear()

        self._running = True
        self.__tasks.append(bot.loop.create_task(self._internal_loop()))

        if wait:
            await self._event.wait()
        log.debug(f"Menu::start - {self.get_title()} - exit")

    async def finalize(self, timed_out):
        """|coro|

        A coroutine that is called when the menu loop has completed
        its run. This is useful if some asynchronous clean-up is
        required after the fact.

        Parameters
        --------------
        timed_out: :class:`bool`
            Whether the menu completed due to timing out.
        """
        return

    async def send_initial_message(self, ctx, channel):
        """|coro|

        Sends the initial message for the menu session.

        This is internally assigned to the :attr:`message` attribute.

        Subclasses must implement this if they don't set the
        :attr:`message` attribute themselves before starting the
        menu via :meth:`start`.

        Parameters
        ------------
        ctx: :class:`Context`
            The invocation context to use.
        channel: :class:`discord.abc.Messageable`
            The messageable to send the message to.

        Returns
        --------
        :class:`discord.Message`
            The message that has been sent.
        """
        submenu_options = self.enumerated_submenus if self.enumerate_submenus else self.submenus

        title = self.get_title()
        initial_msg = self.get_initial_message()

        embed = discord.Embed(title=title,
                              colour=discord.Colour(self.embed_info.colour),
                              description=initial_msg)

        if self.embed_info.thumbnail:
            embed.set_thumbnail(url=self.embed_info.thumbnail)
        if self.embed_info.author:
            embed.set_author(name=self.embed_info.author.name,
                             url=self.embed_info.author.url,
                             icon_url=self.embed_info.author.icon_url)
        if self.embed_info.footer_text:
            embed.set_footer(text=self.embed_info.footer_text)
        for field in self.embed_info.fields:
            embed.add_field(name=str(field.name), value=str(field.value), inline=field.inline)


        options_name = "Please select one of the following options:"
        options_string = "\n".join(f"**{key}** : {value}" for key, value in submenu_options.items())
        additional_options = "**stop** : Return to previous menu\n**exit** : Close this menu"
        options_string = f"{options_string}\n{additional_options}"

        # embed.add_field(name=options_name, value=options_string, inline=False)
        if len(options_string) <= 1024:
            embed.add_field(name=options_name, value=options_string, inline=False)
            options_name = '\u200b'
        else:
            while len(options_string) > 1024:
                mid = 1024
                try:
                    # break_at = mid + min(-options_string[mid::-1].index('\n'), options_string[mid:].index('\n'), key=abs)
                    break_at = mid + -options_string[mid::-1].index('\n')
                except ValueError:  # if '\n' not in s
                    break_at = len(options_string)

                firstpart, options_string = options_string[:break_at], options_string[break_at:]
                embed.add_field(name=options_name, value=firstpart, inline=False)
                options_name = '\u200b'
            embed.add_field(name=options_name, value=options_string, inline=False)

        await channel.send(embed=embed)
        # nav_action = "number" if self.enumerate_submenus else "string"
        # navigate_msg = f"To select an option, please input it's {nav_action} below. " \
        #                f"You may type **EXIT** at anytime to close this menu."
        # # For now we are just doing the channel which evoked it. TODO: Allow PMs
        # return await channel.send(f"{initial_msg}\n{navigate_msg}\n{submenu_options}")

    def get_title(self):
        raise NotImplementedError

    def get_initial_message(self):
        raise NotImplementedError

    def stop(self):
        """Stops the internal loop."""
        self._running = False
        for task in self.__tasks:
            task.cancel()
        self.__tasks.clear()

    def add_submenu(self, submenu):
        if not isinstance(submenu, Submenu):
            raise TypeError("The submenu passed must be a subclass of Submenu")

        if submenu.label in self.submenus:
            raise RuntimeError(f"Submenu already registered: {submenu.label}")

        self._submenus[submenu.label] = submenu

    def submenu(self, label, *args, **kwargs):
        def decorator(func):
            if isinstance(func, Submenu):
                raise TypeError('Func is already a submenu.')
            result = Submenu(label, func, *args, **kwargs)
            self.add_submenu(result)
            return result
        return decorator

    @property
    def exception(self):
        return self._exception



# coding=utf-8
from __future__ import absolute_import

__author__ = "Anderson Silva <ams.bra@gmail.com>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2015 Anderson Silva - AGPLv3 License"

import octoprint.plugin
import octoprint.events
from octoprint.server import printer

from flask import jsonify, make_response

class RPiGPIOPlugin(octoprint.plugin.EventHandlerPlugin,
                  octoprint.plugin.StartupPlugin,
                  octoprint.plugin.AssetPlugin,
                  octoprint.plugin.SimpleApiPlugin,
                  octoprint.plugin.TemplatePlugin,
                  octoprint.plugin.SettingsPlugin):

    def on_after_startup(self):
        self._logger.info("Raspberry Pi GPIO Triggers")

    def get_settings_defaults(self):
        return dict(
          onstart = "self._logger.info('RPiGPIO On Start')",
          oncomplete = "self._logger.info('RPiGPIO On Complete')",
          oncancel = "self._logger.info('RPiGPIO On Cancel')",
          onfail = "self._logger.info('RPiGPIO On Fail')",
          onerror = "self._logger.info('RPiGPIO On Error')",
          onpause = "self._logger.info('RPiGPIO On Pause')",
          onresume = "self._logger.info('RPiGPIO On Resume')",
          onconnection = "self._logger.info('RPiGPIO On Connection')",
          ondisconnection = "self._logger.info('RPiGPIO On Disconnection')",
          onupload = "self._logger.info('RPiGPIO On Upload')"
        )

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False)
        ]

    #def get_template_vars(self):
    #    return dict(month=self.month)

    #def get_assets(self):
    #    return dict(
    #        css=["css/codemirror.css"],
    #        js=["js/codemirror.js", "js/python.js"]
    #    )

    def on_event(self, event, payload):
        """
        Callback for general OctoPrint events.
        """
        onstart = self._settings.get(["onstart"])
        code_onstart = compile(onstart.format(onstart), '<string>', 'exec')

        oncomplete = self._settings.get(["oncomplete"])
        code_oncomplete = compile(oncomplete.format(oncomplete), '<string>', 'exec')

        oncancel = self._settings.get(["oncancel"])
        code_oncancel = compile(oncancel.format(oncancel), '<string>', 'exec')

        onfail = self._settings.get(["onfail"])
        code_onfail = compile(onfail.format(onfail), '<string>', 'exec')

        onerror = self._settings.get(["onerror"])
        code_onerror = compile(onerror.format(onerror), '<string>', 'exec')

        onpause = self._settings.get(["onpause"])
        code_onpause = compile(onpause.format(onpause), '<string>', 'exec')

        onresume = self._settings.get(["onresume"])
        code_onresume = compile(onresume.format(onresume), '<string>', 'exec')

        onconnection = self._settings.get(["onconnection"])
        code_onconnection = compile(onconnection.format(onconnection), '<string>', 'exec')

        ondisconnection = self._settings.get(["ondisconnection"])
        code_ondisconnection = compile(ondisconnection.format(ondisconnection), '<string>', 'exec')

        onupload = self._settings.get(["onupload"])
        code_onupload = compile(onupload.format(onupload), '<string>', 'exec')

        if event == octoprint.events.Events.CONNECTED:
            if code_onconnection != "":
                import RPi.GPIO as GPIO
                exec(code_onconnection)

        if event == octoprint.events.Events.DISCONNECTED:
            if code_ondisconnection != "":
                import RPi.GPIO as GPIO
                exec(code_ondisconnection)

        if event == octoprint.events.Events.UPLOAD:
            if code_onupload != "":
                import RPi.GPIO as GPIO
                exec(code_onupload)

        if event == octoprint.events.Events.PRINT_STARTED:
            if code_onstart != "":
                import RPi.GPIO as GPIO
                exec(code_onstart)

        if event == octoprint.events.Events.PRINT_DONE:
            if code_oncomplete != "":
                import RPi.GPIO as GPIO
                exec(code_oncomplete)

        if event == octoprint.events.Events.PRINT_FAILED:
            if code_onfail != "":
                import RPi.GPIO as GPIO
                exec(code_onfail)

        if event == octoprint.events.Events.PRINT_CANCELLED:
            if code_oncancel != "":
                import RPi.GPIO as GPIO
                exec(code_oncancel)

        if event == octoprint.events.Events.PRINT_PAUSED:
            if code_onpause != "":
                import RPi.GPIO as GPIO
                exec(code_onpause)

        if event == octoprint.events.Events.PRINT_RESUMED:
            if code_onresume != "":
                import RPi.GPIO as GPIO
                exec(code_onresume)

        if event == octoprint.events.Events.ERROR:
            if code_onerror != "":
                import RPi.GPIO as GPIO
                exec(code_onerror)

    ##~~ Softwareupdate hook
    def get_update_information(self):
        return dict(
            rpigpio=dict(
                displayName="Raspberry Pi GPIO Triggers",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="amsbr",
                repo="OctoPrint-RPiGPIO",
                current=self._plugin_version,

                # update method: pip w/ dependency links
                pip="https://github.com/amsbr/OctoPrint-RPiGPIO/archive/{target_version}.zip"
            )
        )


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Raspberry Pi GPIO Triggers"
__plugin_version__ = "1.0"
__plugin_description__ = "Control GPIO pins of your Raspberry Pi on OctoPrint events"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = RPiGPIOPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }

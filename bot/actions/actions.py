from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType, Restarted


class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    async def run(
            self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        events = [SessionStarted(), ActionExecuted("action_listen")]
        dispatcher.utter_message(
            text='Bonjour, je suis AbotHotel votre assistant virtuel. Je suis la pour vous aider à faire une réservation.')

        return events


class ActionRestarted(Action):
    """ This is for restarting the chat"""

    def name(self):
        return "action_restart"

    def run(self, dispatcher, tracker, domain):
        return [Restarted()]

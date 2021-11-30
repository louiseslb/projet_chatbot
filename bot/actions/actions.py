from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType, Restarted

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


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


class ActionResetDates(Action):
    def name(self):
        return "action_reset_dates"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet('date_arrival', None),
                SlotSet('date_departure', None)]


class ActionResetNumberPerson(Action):
    def name(self):
        return "action_reset_number_person"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet('number_person', None)]


class ActionResetMaiil(Action):
    def name(self):
        return "action_reset_mail"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet('mail', None)]


class ValidateHotelForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_hotel_form"

    def validate_date_arrival(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate date arrival value."""

        dispatcher.utter_message(text='')

        return {"date_arrival": slot_value}

    def validate_date_departure(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate date arrival value."""

        tracker.get_slot('date_arrival')
        dispatcher.utter_message(text='')
        return{'date_arrival': None,
               'date_departure': None}


        #return {"date_arrival": slot_value}

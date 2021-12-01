from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType, Restarted

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import re
import datetime

import dateutil.parser as dparser
from dateutil.relativedelta import relativedelta


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

        inputDate = slot_value
        day, month, year = inputDate.split('/')
        isValidDate = True
        try:
            datetime.datetime(int(year), int(month), int(day))
        except ValueError:
            isValidDate = False

        if (isValidDate):
            if datetime.date(int(year), int(month), int(day)) < datetime.date.today():
                dispatcher.utter_message(text='Cette date est déja passée')
                return {"date_arrival": None}
            else:
                return {"date_arrival": slot_value}
        else:
            dispatcher.utter_message(text='La date ne semble pas valide')
            return {"date_arrival": None}

    def validate_date_departure(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate departure value."""
        departureDate = slot_value
        arrivalDate = tracker.get_slot('date_arrival')
        day_departure, month_departure, year_departure = departureDate.split('/')
        day_arrival, month_arrival, year_arrival = arrivalDate.split('/')
        isValidDate = True

        end_date = datetime.datetime(int(year_departure), int(month_departure), int(day_departure))
        start_date = datetime.datetime(int(year_arrival), int(month_arrival), int(day_arrival))

        try:
            datetime.datetime(int(year_departure), int(month_departure), int(day_departure))
        except ValueError:
            isValidDate = False

        if (isValidDate):
            if datetime.date(int(year_departure), int(month_departure), int(day_departure)) < datetime.date(
                    int(year_arrival), int(month_arrival), int(day_arrival)):
                dispatcher.utter_message(text="La date de départ est avant la date d'arrivée. Veuillez les resssaisir")
                return {'date_departure': None,
                        'date_arrival': None}
            elif datetime.date(int(year_departure), int(month_departure), int(day_departure)) == datetime.date(
                    int(year_arrival), int(month_arrival), int(day_arrival)):
                dispatcher.utter_message(text="Vous ne pouvez pas arriver et partir le même jour.")
                return {'date_departure': None}
            elif (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) > 6:
                dispatcher.utter_message(
                    text='Malheureusement, notre hôtel ne peux pas vous accueillir aussi longtemps (Maximum 6 mois)')
                return {'date_departure': None}
            else:
                return {"date_arrival": slot_value}
        else:
            dispatcher.utter_message(text='La date ne semble pas valide')
            return {"date_arrival": None}

    def validate_mail(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate mail value."""
        print('validate mail')

        r = re.compile("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        if r.match(slot_value):
            return {'mail': slot_value}
        else:
            dispatcher.utter_message(text="L'adresse mail saisie semble invalide.")
            return {'mail': None}

    def validate_number_person(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate date arrival value."""
        return {'number_person': slot_value}

# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, ActionExecuted, UserUttered, ReminderScheduled, ReminderCancelled, AllSlotsReset, \
    UserUtteranceReverted, Restarted
from rasa_sdk.forms import FormAction
from typing import Any, Text, Dict, List, Union
import requests, json, sys
import csv

class SearchStoriesForm(FormAction):

    def name(self) -> Text:
        return "search_stories_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["search_text"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "search_text": [self.from_entity(entity="challenge_answer"), self.from_text()],
        }

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        return_data = []

        try:

            search_text = tracker.get_slot("search_text")

            print("search_text::", search_text)

            return_data  =  return_data + [SlotSet("search_text", None)]

            # defining the api-endpoint  
            API_ENDPOINT = "http://localhost:65482/api/search"
            
            headers = {'content-type': 'application/json'}

            # data to be sent to api 
            data = {"top_k":5,"mode":"search","data":[search_text]}
            
            # sending post request and saving response as response object 
            r = requests.post(url = API_ENDPOINT, data=json.dumps(data), headers=headers)

            # extracting response text  
            pastebin_url = r.text 
            #print("The pastebin URL is:%s"%pastebin_url) 

            with open('data/db_books.csv', newline='') as f:
                reader = csv.reader(f)
                csv_data = list(reader)

            json_response =  json.loads(pastebin_url)
            buttons = []
            #print(json_response["search"])
            #print(json_response["search"]["docs"])
            json_list = json_response["search"]["docs"][0]["matches"]
            #print(json_list)
            for result in json_list:
                if result and "parentId" in result:
                    print(result["parentId"])
                    print(result["text"])
                    print(csv_data[result["parentId"]])
                    #text = result["text"]

                    #text = SearchStoriesForm.remove_prefix(result["text"], "txt,")
                    text = csv_data[result["parentId"]][1]
                    story_id = csv_data[result["parentId"]][0].replace(".txt", "")
                    author = csv_data[result["parentId"]][2]
                    language = csv_data[result["parentId"]][3]
                    link = "https://www.gutenberg.org/ebooks/" + story_id

                    button = { 
                        "title": text,
                        "url": link,
                        "type": "web_url"
                    }
                    print(button)
                    buttons.append(button)

            print(buttons)

            search_carousel = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [{
                    "title": "Search Results",
                    "subtitle": "using Jina AI",
                    "image_url": "/static/jina.png",
                    "buttons": buttons
                    }
                    ]
                }
             }
            dispatcher.utter_message(attachment=search_carousel)

            
        except:
            print("error occurred :: ", sys.exc_info()[0])

        return return_data

    @staticmethod
    def remove_prefix(text, prefix):
        return text.replace(prefix, "")


if __name__ == "__main__":
   SearchStoriesForm.remove_prefix("txt, The Queen of Spades and other stories, Alexander Pushkin, English", ".txt,")


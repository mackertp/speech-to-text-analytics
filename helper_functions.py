"""
Methods for using the IBM Watson cloud STT engine and dealing with returning JOSN, uses the IBM tonal
analysis and personality insights features as well.

@author Preston Mackert
"""

# ---------------------------------------------------------------------------------------------------- #
# imports 
# ---------------------------------------------------------------------------------------------------- #

import json
import os
from os.path import join, dirname
import config
from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import PersonalityInsightsV3


# ---------------------------------------------------------------------------------------------------- #
# support functions for speech to text
# ---------------------------------------------------------------------------------------------------- #

def get_transcript(audio_file_name, file_type, folder):
    """ given an audio file and file type, outputs the file into a json file using IBM watson SDK
    https://github.com/watson-developer-cloud/python-sdk/blob/master/examples/speech_to_text_v1.py """
    speech_to_text = SpeechToTextV1(username=config.stt_uname, password=config.stt_pword, url=config.stt_url)

    # opens the audio file and gathers the transcript result with word confidence
    with open(join(dirname(os.getcwd() + "/" + folder + "/"), audio_file_name), "rb") as audio_file:
        result = json.dumps(speech_to_text.recognize(audio=audio_file, content_type="audio/" + file_type,
                                                     timestamps=False, word_confidence=True), indent=2)

    # writes the result into a json file
    output_filename = audio_file_name.replace(file_type, "json")
    with open(output_filename, "w") as outfile:
        json.dump(result, outfile)


# ---------------------------------------------------------------------------------------------------- #

def send_batch(folder):
    """ takes a folder of audio files and converts them all into json transcripts """
    try:
        for audio_file in os.listdir(folder):
            filename, file_extension = os.path.splitext(audio_file)
            file_extension = file_extension.replace(".", "")
            print("transcribing " + filename + "." + file_extension + "...")
            get_transcript(filename + "." + file_extension, file_extension, folder)

    except:
        print("invalid folder")


# ---------------------------------------------------------------------------------------------------- #

def convert_json_to_data(json_file):
    """ takes in a json file and reads it into pythonic data, reformated for easier reading """
    json_data = json.loads(open(json_file).read())
    formatted_dict = json.loads(json_data)
    results = formatted_dict.get("results")

    # watson's json response breaks data up into partial dictionaries and needs to be restitched
    word_confidence_hub = []
    partial_confidence_hub = []
    full_transcript = ""
    chunks = []

    # commence the stitching
    for partial_dict in results:
        # each partial dict has two values. first is the content, second is boolean True
        alternatives = partial_dict.get("alternatives")[0]

        # gather all of the partial content
        word_confidence = alternatives.get("word_confidence")
        partial_confidence = alternatives.get("confidence")
        partial_transcript = alternatives.get("transcript")

        # stitch partial content into larger data sets
        partial_confidence_hub.append(partial_confidence)
        full_transcript += partial_transcript
        # the word confidence is nested... un-nesting it
        for word in word_confidence:
            word_confidence_hub.append(word)

        # add the partial_dict for reference purposes
        chunks.append(partial_dict)

    # calculating the overall confidence level from partial confidences
    confidence = sum(partial_confidence_hub) / len(partial_confidence_hub)

    # reconstructing the dictionary into something more useful and returning
    return {"transcript": full_transcript, "confidence": confidence, "words": word_confidence_hub, "chunks": chunks}


# ---------------------------------------------------------------------------------------------------- #
# support functions for tone analysis 
# ---------------------------------------------------------------------------------------------------- #

def analyze_tone(text):
    """ given some text, send it to IBM Watson's tone analysis tool
    https://github.com/watson-developer-cloud/python-sdk/blob/master/examples/tone_analyzer_v3.py """
    tone_analyzer = ToneAnalyzerV3(username=config.tone_uname, password=config.tone_pword, url=config.tone_url,
                                   version=config.tone_vers)

    json_data = json.dumps(tone_analyzer.tone(tone_input=text, content_type="text/plain"), indent=2)
    formatted_dict = json.loads(json_data)
    tones = format_tone(formatted_dict)
    return tones


# ---------------------------------------------------------------------------------------------------- #

def format_tone(data):
    """ deconstructing the dictionary returned into just the tones and their scores """
    tone_dict = data["document_tone"]
    tone_dict = tone_dict["tones"]
    new_dict = {}
    for tone in tone_dict:
        tone_name = tone["tone_name"]
        tone_score = tone["score"]
        new_dict[tone_name] = tone_score

    return new_dict


# ---------------------------------------------------------------------------------------------------- #
# support functions for personality insights
# ---------------------------------------------------------------------------------------------------- #

def analyze_personality(text):
    """ given some text, send it to IBM Watson's personality insight tool, requires at least 100 words
    https://github.com/watson-developer-cloud/python-sdk """
    personality_insights = PersonalityInsightsV3(version=config.pi_ver, username=config.pi_uname,
                                                 password=config.pi_pword, url=config.pi_url)
    json_data = json.dumps(
        personality_insights.profile(text, content_type='text/plain', raw_scores=True, consumption_preferences=True),
        indent=2)
    formatted_dict = json.loads(json_data)
    personality_profile = format_personality(formatted_dict)
    return personality_profile


# ---------------------------------------------------------------------------------------------------- #

def format_personality(formatted_dict):
    """ taking the entire formatted dictionary from the JSON, deconstruct it into something readable """
    # these are hardcoded because these are always going to be the keys... unless IBM changes it, then
    # check this by printing out the formatted_dict
    personality = formatted_dict["personality"]
    needs = formatted_dict["needs"]
    values = formatted_dict["values"]
    con_prefs = formatted_dict["consumption_preferences"]

    personality_dicts = {}
    needs_dict = {}
    values_dict = {}
    con_pref_dict = {}

    # deconstructing the personality
    for key in personality:
        name = key["name"]
        percent = key["percentile"]
        children = key["children"]
        reformatted_children = {}
        for child in children:
            child_name = child["name"]
            child_percent = child["percentile"]
            reformatted_children[child_name] = child_percent
        personality_dicts[name] = [percent, reformatted_children]

    # deconstructing the needs
    for key in needs:
        name = key["name"]
        percent = key["percentile"]
        needs_dict[name] = percent

    # deconstructing the values
    for key in values:
        name = key["name"]
        percent = key["percentile"]
        values_dict[name] = percent

    # deconstructing consumption preferences
    for key in con_prefs:
        name = key["name"]
        prefs = key["consumption_preferences"]
        pref_dict = {}
        for key in prefs:
            pref_name = key["name"]
            pref_score = key["score"]
            pref_dict[pref_name] = pref_score
        con_pref_dict[name] = pref_dict

    # returning easier format
    formatted_personality = {"personality": personality_dicts, "needs": needs_dict, "values": values_dict,
                             "con_prefs": con_pref_dict}

    return formatted_personality

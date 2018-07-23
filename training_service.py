import sys
import base64
import requests


def get_wave(fname):
    with open(fname) as infile:
        return base64.b64encode(infile.read())


endpoint = "https://snowboy.kitt.ai/api/v1/train/"


############# MODIFY THE FOLLOWING #############
token = "09a5160decf111feb9a6d5ae2251ed099f31b6e9"
hotword_name = "sweater"
language = "en"
age_group = "30_39"
gender = "M"
microphone = "usb microphone"
############### END OF MODIFY ##################

if __name__ == "__main__":
    try:
        [_, sweater1, sweater2, sweater3, out] = sys.argv
    except ValueError:
        print "Usage: %s wave_file1 wave_file2 wave_file3 out_model_name" % sys.argv[0]
        sys.exit()

    data = {
        "name": hotword_name,
        "language": language,
        "age_group": age_group,
        "gender": gender,
        "microphone": microphone,
        "token": token,
        "voice_samples": [
            {"wave": get_wave(sweater1)},
            {"wave": get_wave(sweater2)},
            {"wave": get_wave(sweater3)}
        ]
    }

    response = requests.post(endpoint, json=data)
    if response.ok:
        with open(out, "w") as outfile:
            outfile.write(response.content)
        print "Saved model to '%s'." % out
    else:
        print "Request failed."
print response.text

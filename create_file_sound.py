
import argparse

from Process.Util.Util import Util

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('id', help='id image')
args = parser.parse_args()


id_audio = int(args.id)


Util().save_audio_show(id_audio)


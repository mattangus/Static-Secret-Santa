from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import random
import argparse

parser = argparse.ArgumentParser(description='Generate javascript and links for a secret santa page')
parser.add_argument('input', metavar='<names file>', type=str, nargs=1,help='input file with names')
parser.add_argument('js_out', metavar='<javascript file>', type=str, nargs=1,help='output file for generated javascript')
parser.add_argument('l_out', metavar='<links file>', type=str, nargs=1, help='output file for generated links')

args = parser.parse_args()

def getNames(file):
	with open(file) as f:
		content = f.readlines()
	content = [l.replace('\r\n','') for l in content]
	return content

def rotate(l,n):
	return l[n:] + l[:n]

def generate_pairs():
	names = getNames(args.input[0])
	random.shuffle(names)
	rot = rotate(names[:],1)
	keys = [rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend()) for i in range(len(names))]
	pairs = [{'giver':names[i],'recipient':rot[i], 'key':keys[i]} for i in range(len(names))]
	return pairs

pairs = generate_pairs()
for i in range(len(pairs)):
	cur = pairs[i]
	public_key = cur['key'].public_key()
	ciphertext = public_key.encrypt(
		bytes(str.encode(cur['recipient'])),
		padding.OAEP(
		mgf=padding.MGF1(algorithm=hashes.SHA1()),
		algorithm=hashes.SHA1(),
		label=None
		)
	)
	
from iota import Iota
from iota.crypto.addresses import AddressGenerator
from datetime import datetime
import iota
import json
import random

def checknodestate():
	api = Iota("https://field.deviota.com:443")	
	nodeinfo = api.get_node_info()
	latestmilestone = (nodeinfo['latestMilestoneIndex'])
	latestsubtanglemilestone = (nodeinfo ['latestSolidSubtangleMilestoneIndex'])
	print(str(latestmilestone) + " " + str(latestsubtanglemilestone))
	if latestmilestone - latestsubtanglemilestone > 3:
		return 2
	else:
		return 1

#Generate addresses with a security level of 2 (the usual for most wallets)
def generator():
	
	chars=u'9ABCDEFGHIJKLMNOPQRSTUVWXYZ' #27 characters - max number you can express by one Tryte - do you remember?
	rndgenerator = random.SystemRandom()

	MySeed = u''.join(rndgenerator.choice(chars) for _ in range(81))

	generator = AddressGenerator(seed=MySeed, security_level=2)
	addresses = generator.get_addresses(0, 3) #index, count
	return(addresses)

def createtransactions(addresses):
	addresses = addresses
	now = datetime.now()
	api = Iota("https://field.deviota.com:443")
	for newaddress in addresses:
		pt = iota.ProposedTransaction(	address=iota.Address(newaddress),
										value=0,
										#Tag needs to be 27 chars
										tag=iota.Tag(b''),
										message=iota.TryteString.from_unicode(' = ' + str(now))
										)
		print("\nTransaction preparing")
		# Lick the stamp and send it
		Bundle = api.send_transfer(depth=3,transfers=[pt],min_weight_magnitude=14)['bundle']
		print("\nBundle Hash :" + str(Bundle.hash))
		print("\nTail transactions in the bundle is a TX :" + str(Bundle.tail_transaction.current_index))

		print("\nAll transactions in this bundle: \n")
		for txn in Bundle:
			print(vars(txn))
			print("")

if __name__ == "__main__":
	nodesync = checknodestate()
	if nodesync == 1:
		print("Node is healthy")
	else:
		print("Node is probably out of sync")
		Exit()
	txaddresses = generator()
	createtransactions(txaddresses)
	"Done"


	

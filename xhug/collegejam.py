import urllib.request
import json
import dml
import prov.model
import datetime
import uuid


class collegejam(dml.Algorithm):
	contributor = 'xhug'
	reads = ['xhug.trafficejam','xhug.bostoncolleges']
	writes = ['xhug.collegeandjam']


def union(R, S):
    return R + S

def difference(R, S):
    return [t for t in R if t not in S]

def intersect(R, S):
    return [t for t in R if t in S]

def project(R, p):
    return [p(t) for t in R]

def select(R, s):
    return [t for t in R if s(t)]
 
def product(R, S):
    return [(t,u) for t in R for u in S]

def aggregate(R, f):
    keys = {r[0] for r in R}
    return [(key, f([v for (k,v) in R if k == key])) for key in keys]



	@staticmethod
	def execute(trial = False):


		startTime = datetime.datetime.now()
		client = dml.pymongo.MongoClient()
		repo = client.repo
		repo.autenticate("xhug", "xhug")
		jam = repo.xhug.trafficejam
		colleges = repo.xhug.bostoncolleges

		'''cleanse the data to contain only the streets of jam
		'''

		jamlocations = project(jam, lambda v: (v[street]))

		def getschooladdress(school):
			if 'Address' in school:
				return school['properties']['Address']

		collegelocations = project(colleges, getschooladdress())
	
		


		
		

		'''computing the frequency of the jam occurs on each street
		'''

		jamstreets = aggregate(project(X, lambda t: (t[0]), sum))
			

		
		schoolsstreet= []

		'''cleanse the data to contain only streets of schools
		'''
		for x in schoolsData.find():
			if 'Name' && 'Address' && in x:
			schoolsstreet.append(entry['Name'],entry['Address'])


		

		'''aggregate two new created dataset jamstreets and schoolsstreet into 
		   a new one jamandschools which has the attributes Name, Street and 
		   Frequency. 
		'''

		jamandschools = []

		jamandschools = [(x[0],y[1]) for x in schoolsstreet for y in jamstreets if y[0] in x[1]]




		

		repo.dropCollection("jamandschoolsdata")
		repo.createCollection("jamandschoolsdata")
		repo.['xhug.jamandschoolsdata'].insert_many(jamandschools)
		repo.logout()
		endTime = datetime.datetime.now()
		return {"start": startTime, "end": endTime}

		@staticmethod
		def provenance(doc = prov.model.ProvDocument(), startTime = None, endTime = None):
			client = dml.pymongo.MongoClient()
			repo = client.repo
			repo.authenticate("xhug", "xhug")
			doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format.
			doc.add_namespace('dat', 'http://datamechanics.io/data/') # The data sets are in <user>#<collection> format.
			doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
			doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
			doc.add_namespace('bdp', 'https://data.cityofboston.gov/resource/')
			this_script = doc.agent('alg:xhug#jamandschools', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
			resource_jam = doc.entity('dat:xhug#jam', {'prov:label':'JAMDATA', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
			resource_schools = doc.entity('dat:xhug#schools', {'prov:label':'SCHOOLSDATA', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
			get_jamandschoolsdata = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime, {prov.model.PROV_LABEL:'jamandschools', prov.model.PROV_TYPE:'ont:DataSet'})
			doc.wasAssociatedWith(get_jamandschoolsdata, this_script)
			doc.usage(get_jamandschoolsdata, resource_schools, startTime,None, {prov.model.PROV_TYPE: 'ont:Computation'})
			doc.usage(get_jamandschoolsdata, resource_jam, startTime,None, {prov.model.PROV_TYPE: 'ont:Computation'})
			JS = doc.entity('dat:xhug#jamandschoolsdata', {prov.model.PROV_LABEL:'JAMSCHOOL', prov.model.PROV_TYPE:'ont:DataSet'})
			doc.wasAttributedTo(JS, this_script)
			doc.wasGeneratedBy(JS, get_jamandschoolsdata, endTime)
			doc.wasDerivedFrom(JS, resource_jam, get_jamandschoolsdata, get_jamandschoolsdata, get_jamandschoolsdata)
			doc.wasDerivedFrom(JS, resource_schools, get_jamandschoolsdata, get_jamandschoolsdata, get_jamandschoolsdata)

			repo.logout()
			return doc

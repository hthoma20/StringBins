from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from uuid import uuid1
from os import path, mkdir

BIN_ALREADY_EXISTS_EXCEPTION = HTTPException(status_code=400, detail='Bin Already Exists')
NAME_UNSPECIFIED_EXCEPTION = HTTPException(status_code=400, detail='Name Unspecified')
BIN_NOT_FOUND_EXCEPTION = HTTPException(status_code=404, detail='Bin Not Found')

BIN_ROOT = './stringbins'

app = FastAPI()


class Content(BaseModel):
	content: str


@app.post("/create")
def create(name: str = '', uuid : bool = False):
	
	if name == '' and not uuid:
		raise NAME_UNSPECIFIED_EXCEPTION

	bin_to_create = bin_name(name, uuid)

	if bin_exists(bin_to_create):
		raise BIN_ALREADY_EXISTS_EXCEPTION

	create_empty_bin(bin_to_create)
	return {
		'bin-name': bin_to_create
	}


@app.get('/retrieve')
def retrieve(name: str):
	if not bin_exists(name):
		raise BIN_NOT_FOUND_EXCEPTION

	return get_bin_content(name)

@app.put('/update')
def update(name: str, content: Content):
	if not bin_exists(name):
		raise BIN_NOT_FOUND_EXCEPTION

	write_to_bin(name, content.content)


def bin_name(name: str, uuid: bool):
	# Both should not be empty
	assert name != '' or uuid

	if uuid:
		if name != '':
			return '{}-{}'.format(name, uuid1())

		return str(uuid1())


	return name

def file_name(bin_name: str):
	return '{}/{}.txt'.format(BIN_ROOT, bin_name)

def bin_exists(name: str):
	return path.exists(file_name(name))

def create_empty_bin(name: str):
	write_to_bin(name, '')

def write_to_bin(name: str, content: str):
	with open(file_name(name), 'w') as file:
		file.write(content)

def get_bin_content(name: str):
	with open(file_name(name), 'r') as file:
		return file.read()
        
def create_bin_root():
    if not path.isdir(BIN_ROOT):
        print('Root dir {} does not exist, creating it'.format(BIN_ROOT))
        mkdir(BIN_ROOT)
        return
    
    print('Root dir {} already exists'.format(BIN_ROOT))
        
if __name__ == '__main__':
    PORT = 5867
    RELOAD = True
    
    create_bin_root()
    uvicorn.run('main:app', port=PORT, reload=RELOAD)

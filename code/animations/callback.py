from alive_progress import alive_bar
## TEST for progress bar
# WIP. TODO

def compute():
    for i in range(1000):
        ... # process items as usual.
        yield  # insert this :)

def save_cb(current:int, total:int):    
    """ Callback function to track progress during the saving process. """
    if current%100 == 0: print(f'Saving frame {current} of {total}')
    with alive_bar(total) as bar:
        for current in range(total):
            bar()
        
with alive_bar(1000) as bar:
    for i in compute():
        bar()
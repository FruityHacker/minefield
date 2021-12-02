#path.py
#By Max Morningstar
#A python program to pass the F-Secure Minefield sandbox challenge. Establishes
#     a connection to the Minefield site and downloads the site HTML. HTML is
#     parsed into a 2d array, then a path is recursively found. The correct
#     path is then automatically submitted back to the site, and the resulting
#     success page's HTML is printed to the console to access the flag.
import requests

#function pathfinder
#recursive function that determines a path through a 22x22 2D matrix
#inputs: row and col, integers
#returns: 0 or 1 (true or false)
def pathfinder(row, col):
    #define array and solution as global so they can be modified
    global arr
    global sol

    #check if out-of-bounds
    if (row < 0 or row > 21):
        return 0
    if (col < 0 or col > 21):
        return 0

    if (arr[row][col] == 2): #if at finish
        return 1
    if (arr[row][col] == 1): #if at mine
        return 0
    if (arr[row][col] == 4): #if at deadend node
        return 0
    if (arr[row][col] == 3): #if at seen node
        return 0

    #if at valid space or start
    if (arr[row][col] == 0 or arr[row][col] == 5):
        arr[row][col] = 3
        #search up
        if (pathfinder(row-1,col)):
            sol = sol + "U"
            return 1
        #search right
        if (pathfinder(row,col+1)):
            sol = sol + "R"
            return 1
        #search down
        if (pathfinder(row+1,col)):
            sol = sol + "D"
            return 1
        #search left
        if (pathfinder(row,col-1)):
            sol = sol + "L"
            return 1
    #if no path found, mark node as dead end and return
    arr[row][col] = 4
    return 0

#establish connection
session = requests.Session()
page = session.get('https://pg-0451682683.fs-playground.com/', verify=False)
mine_string = page.text


#create array
arr = [[0 for i in range(22)] for j in range(22)]

#initialize variables
index = 0
mine_end = len(mine_string) - 1

#initialize the array
for (i,row) in enumerate(arr):
    for (j,value) in enumerate(row):
        curr_empty = mine_string.find('empty', index, mine_end)
        curr_full = mine_string.find('full', index, mine_end)
        if curr_empty == -1:
            arr[i][j] = 1
        elif curr_full == -1:
            arr[i][j] == 0
        elif curr_empty < curr_full:
            arr[i][j] = 0
            index = curr_empty + 1
        elif curr_empty > curr_full:
            arr[i][j] = 1
            index = curr_full + 1

#hard code end as 2 for search algorithm
arr[21][21] = 2
#hard code start for search algorithm
arr[0][0] = 5

#initialize variables
row = 0
col = 0
sol = ""

#main maze solving loop, starting from origin
pathfinder(0, 0)

#invert solution string
sol = sol[::-1]
#submit string
sol_url = 'https://pg-0451682683.fs-playground.com/Solution/Submit?solution=' + sol
sol_html = session.get(sol_url, verify=False)
success = sol_html.text
#print HTML for flag retrieval
print(success)

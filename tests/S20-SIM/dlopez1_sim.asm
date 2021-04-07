# start and end of the locations array
assigni $1 20
assigni $2 40

# assignign random locations to 20 people in our grid
assigningLocations:
assigni $7 39
beq $1 locationsSet
# setting our upper and lower bounds to for the random number that
# we want to generate when getting a random number <= 100
# we have to do this because of bitmasking
assigni $5 99
assigni $4 1
getRandom:
rand $6 127
sgt $6 $5
beq $4 getRandom
# at this point register $6 has the random value
store $6 $1
out $4 $6
# looping to the next index that we want to assign a random location
addi $1 1
# looping unconditionally
beq $7 assigningLocations
locationsSet:
# loading the first element of the locations array into the first infection element
# this represents the first person getting the sickness.
assigni $0 20
load $3 $0
assigni $0 0
# loading the first value of the locations array into the infections array
store $3 $0
# $0 will have our looping index in the infection array
assigni $0 1
while:
assigni $7 20
beq $0 endOfArray
# ignoring if the element is empty (storing a zero)
assigni $7 0
load $3 $0
beq $3 empty
# if the element is not empty, then we will move it randomly
# to avoid having to have a wrapping function, the tryAgain
# label is to keep on trying until we get a random value
# tha lets us stay in the grid.
tryAgain:
# generating the random number from 0-3 and moving accordingly
rand $4 3
assigni $7 0
# turning the light off before we move
out $7 $3
assigni $7 0
beq $4 moveUp
assigni $7 1
beq $4 moveDown
assigni $7 2
beq $4 moveLeft
assigni $7 3
beq $4 moveRight

moveUp:
addi $3 -10
assigni $7 0
sgt $7 $3
addi $3 10
assigni $6 1
# if the number made us leave the grid, then we
# try to generate another random number
beq $6 tryAgain
addi $3 -10
# updating the infected array and the locations array
store $3 $0
addi $0 20
store $3 $0
addi $0 -20
assigni $7 1
# displaying the change in location of the infected person
out $7 $3
# $6 will have the value of j
assigni $6 20
assigni $7 40
beq $7 loop
moveDown:
addi $3 10
assigni $7 99
sgt $3 $7
addi $3 -10
assigni $6 1
# if the number made us leave the grid, then we
# try to generate another random number
beq $6 tryAgain
addi $3 10
# updating the infected array and the locations array
store $3 $0
addi $0 20
store $3 $0
addi $0 -20
assigni $7 1
# displaying the change in location of the infected person
out $7 $3
# $6 will have the value of j
assigni $6 20
assigni $7 40
beq $7 loop
moveLeft:
addi $3 -1
assigni $7 0
sgt $7 $3
addi $3 1
assigni $6 1
# if the number made us leave the grid, then we
# try to generate another random number
beq $6 tryAgain
addi $3 -1
# updating the infected array and the locations array
store $3 $0
addi $0 20
store $3 $0
addi $0 -20
assigni $7 1
# displaying the change in location of the infected person
out $7 $3
# $6 will have the value of j
assigni $6 20
assigni $7 40
beq $7 loop
moveRight:
addi $3 1
assigni $7 99
sgt $3 $7
addi $3 -1
assigni $6 1
# if the number made us leave the grid, then we
# try to generate another random number
beq $6 tryAgain
addi $3 1
# updating the infected array and the locations array
store $3 $0
addi $0 20
store $3 $0
addi $0 -20
assigni $7 1
# displaying the change in location of the infected person
out $7 $3
# $6 will have the value of j
assigni $6 20
assigni $7 40
beq $7 loop
loop:
# at this point we have $3 with the value of the infected person
# and we will loop throught the location array to see if any location is the
# same
# beq is checking if we reached the end of the locations array
beq $6 empty
load $7 $6
# infecting if the data is the same
beq $3 infected
beq $7 wrapUp
infected:
# getting the locations index j to store the location data
# at j in infections[j]
assigni $4 -20
add $4 $6
store $3 $4
assigni $7 1
# updating the display
out $7 $3
wrapUp:
# updating j
assigni $7 40
addi $6 1
beq $7 loop
empty:
# looping back to the next index in the infections array
addi $0 1
beq $7 while

endOfArray:
# once we reach the end of the array, we will loop back in
# the infections array
assigni $0 0
beq $7 while

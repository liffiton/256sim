# Author: Ryan Jonas

# Assumptions: 
#    Button input comes from Address 0 in memory
#    LED positions are Addresses 0 to 99 in memory
#    Use $15 as implicit register for comparisons

# Notes:
#    Current direction stored in $7
#      1 means lighting up from 0 to 99
#      0 means turning off from 99 to 0
#    Current LED stored in $2

  seti $2 0           # Start at first LED

lightup:
  set $7 $one         # Direction = 1
  seti $15 100
  beq $2 change       # If current address is 100, out of LED range, branch to change direction
  store $2 $one       # Can now store a 1 in current LED spot
  add $2 $one         # Then increment address to go on to next LED
  set $15 $zero       # Set implicit reg to 0 to loop
  beq $zero input     # Jump back to check for new inputs
  
backwards:
  set $7 $zero        # Direction = 0
  seti $15 0
  beq $2 change       # If current address is 0, next will be out of LED range, branch to change direction
  store $2 $zero
  sub $2 $one
  set $15 $zero       # Set implicit reg to 0 to loop
  beq $zero input     # Jump back to check for new inputs

input:
  set $15 $zero
  set $3 $zero        # Address 0 (Input address)
  load $4 $3          # Load value from Input address
  bgt $4 change       # If Input has changed from 0, change direction
  beq $zero same      # If input didn't change, keep going same direction

change:
  set $15 $zero       # Will compare to 0
  beq $7 lightup      # If direction is 0 (turning off), change to lightup
  set $15 $one        # Then compare to 1
  beq $7 backwards    # If direction is 1, change to backwards
  
same:
  set $15 $zero       # Will compare to 0
  beq $7 backwards    # If direction is 0 (turning off), continue backwards
  set $15 $one        # Then compare to 1
  beq $7 lightup      # If direction is 1, continue lightup
  

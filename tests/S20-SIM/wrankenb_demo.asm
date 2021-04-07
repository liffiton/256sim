#section that turns on lights in sequential order until 99, or from point when button was pressed
Light:
  #special register is set to 0 
  ASSIGNI $7 0
  
  #takes inputs from all the buttons and stores them first 4 registers
  IN $0 $0
  IN $1 $1
  IN $2 $2
  IN $3 $3
  
  #stores total values of all inputs into single register $0
  ADD $0 $1
  ADD $0 $2
  ADD $0 $3
  
  #BNE is used to see if any buttons have been pressed. If the value of $0 is not 0 like $7, then it means a button has been pressed and should branch
  BNE $0 Off
  
  #after above comparison, sets special register to value of 99 and compares against current value for the light
  ASSIGNI $7 99
  BEQ $4 Off
  
  #outputs the current LED to light and then increments $4 to use for the next light
  ASSIGNI $1 1
  OUT $1 $4
  ADDI $4 1
  
  #will always branch back to light because $7 = $7 always
  BEQ $7 Light

#section that turns lights off from 99 to 0, or from the point when a button was pressed to 0
Off:
  #Assigns $7 to 0 since it is intially the value we are working to reach
  ASSIGNI $7 0
  
  #these next 9 lines to the same as in Light block, tests to see if button is pressed in order to branch
  IN $0 $0
  IN $1 $1
  IN $2 $2
  IN $3 $3  
  
  ADD $0 $1
  ADD $0 $2
  ADD $0 $3
  
  BNE $0 Light
  
  OUT $1 $4
  #increments value of current LED by -1 since immediate values are 2's complement
  ADDI $4 -1
  
  # return to Light section if we've reached address 0
  BEQ $4 Light
  
  #always branch back to off because $7 = $7 always
  BEQ $7 Off
 

# A simple program to test DMEM
  assigni $1 0  # current location
  assigni $2 0  # current value
  assigni $7 0  # comparison value for branches
outer:
  addi $2 1 # value++
inner:
  store $2 $1
  addi $1 1
  beq $1 outer
  beq $7 inner

VARIABLE DICT: {key: 0}

#1

BOX()
You are going to test this dialog module by playing 'Escape'.
All will happen on this little pygame window. Press 'A' key for continuing, and use up and down arrows for selecting between options.
If you are a PCBS instructor, make sure to read the README file before, and don't forget to look at the text file too (before or after)!

BOX(You)
...

Where am I?

What happened?

BOX()
A loud noise just woke you up. You are lying on the ground, in a small, empty room.

BOX(You)
I don't remember a thing... I was living my boring everyday life, and then...

And then...?

And then I realize that putting too much dialog would make the game too long.

Okay, for now, let's get out of here. I don't like the vibe of the place.

NEXT(2)


#2 - Initial room
BOX()
The room is completely empty. All there is is a big window and a door.

CHOICE()
Look at the window
Leave the room

NEXTCHOICE(3, 4)


#3 - Look at the window
BOX()
You look at the window.

You can see a beautiful bluish sky. You must be very high.

Down there, there is... Nothing?

BOX(You)
How convenient.

NEXT(2)


#4 - Leave the room
BOX()
A long corridor. Strangely, there is only one other door, at the left corner.
There is also an elevator at the right corner.

CHOICE()
Open the door at the left corner
Enter the elevator

NEXTCHOICE(7, 5)


#5 - Elevator
BOX()
You enter the elevator.

BOX(You)
Okay, let's hit the ground floor button!

NEXTCOND(ISGREATER(key, 0), 14, 6))


#6 - Elevator without key

BOX(You)
Wait, it doesn't work.
There is a keyhole, I think I need a key to make it work.

There a so many possibility in this game, how can I ever find the key...

CHOICE()
Go to the left room
Go to the room at the left

NEXTCHOICE(7, 7)


#7 - Left room
BOX()
You enter the left room.
It smells coffee.

The room is empty... Wait, there is a key lying on the ground.

BOX(You)
I wonder what the key is for ?...

NEXT(8)


#8 - The key

CHOICE()
Take it
Leave it

NEXTCHOICE(10, 9)


#9 - Loop
BOX()
Come on, don't you ever play videogames?

NEXT(8)


#10 
BOX()
You put the key in your pocket.

SIMPLEASSIGNMENT(key, 1)

NEXT(11)


#11 - Almost finished
BOX(You)
What can I do, now?

CHOICE()
Go to the evelator
Definitely go to the elevator

NEXTCHOICE(12, 13)


#12 - Go to the evelator
BOX()
You go to the elevator.

NEXT(5)


#13 - Definitely go to the elevator
BOX()
You definitely go to the elevator.

NEXT(5)


#14 - End!
BOX()
There is a keyhole in the evelator pannel.

You cleverly put the key in the keyhole.

BOX(You)
Let's ride.

BOX(Elevator)
Fzzzzzzzzzzzzzt

Beeep

BOX()
The elevator door opens.

BOX(You)
I am free! The future is forward! Sky is the limit!

BOX()
You did it!
You will never know where you are and why you were there, but your life seems brighter now.

How was it? (satisfactory survey)

CHOICE()
I never had so much fun in my life
This project definitely deserves full marks

BOX()
Stay tuned for my video game in two years!


NEXTEND
# Type-Trainer

If the text is flashing please open an issue, i used the flashing formated text because it didn't flash in my terminal and had a nice color

## Usage

 - put "word" file (list of words. separated by newlines) into cloned repository
 - execute "Word Prepare.py" to prepare savefile (has option to go through the first x words in order)
 - execute "Type Trainer.py" to generate config and start program up
 - you have to resize the terminal beforhand, otherwise it gets fussy
 - enjoy

## Display meaning

### Top from left to right:

 - average seconds per character (Calculated by '(999 * old_speed + speed_for_character) / 1000')
 - average seconds per character for current word (Calculated by '(19 * old_speed + new_speed) / 20')
 - second per character for current word (starting from as soon as you enter the first character, ending as soon as you swich to next word. If you haven't entered the first character yet it displays the final speed of the last word)
 - Score (calculated by 'average of the avetage seconds per character of all used words ^ 3 * the square root of total attempted words')

### Middle from left to right:

 - Total tries
 - Position of the internal counter (goes up unti it finds next word [when 'counter % word["priority"] == 0'])
 - Priority of last word after entering
 - Priority of current word

the lower the priorty value the more likeley the word will be pickes

As a refferece how much the score is worth:<br />
I've been touch typing for about a week, got an average of 1/3 seconds per character with 1900 total attempts -> 5000

Electricity and heat are dangerous! Evaluate the risk and make go no go decision!

Web-based Raspberry Pi Kiln Control:
- achieved my goal to run on Rasberry Pi Zero W, but I am currently running on a Raspberry Pi 3b: 
	+ sqlite3 instead of MySQL
	+ lighttpd instead of apache2 (apache memory was 1/2 pi zero memory, lighttpd does not even show up in top)
	+ on a Pi Zero W 'startx chromium-browser --start-maximized' (chrome in X with no window manager)
    + or hit it with browser from other machine on your network
    + I run full desktop on Pi 3b

- kiln sitter(KS) as a sensor
	+ KS functions as 'ARMED', can not start firing without kilnsitter being armed
	+ mode 1: set top temp lower than KS cone, thermocouple temp is shutoff trigger, KS is safety
	+ mode 2: set top temp higher than KS cone, KS is shutoff trigger, thermocouple is safety

Future improvements:
- record ambient temp with firing data:
- thermocouple class:
	+ MAX31855 current harware,
	+ MAX31856 has 50/60hz filter and a correction table and can do multiple types including S, minimal change
- performance watchdog:
	+ warning notifications, klexting;
	+ shutdown when a minimum rate cannot be maintained,
- inductive current sensors: element fault indication;
- zone control: thermocouple/section and control sections independently;
- crash/loss of power recovery:
	+ PI comes up, KS is armed & profile is 'Running' then how to consider unfinished segment
	+ compare temp at the timestamp to current temp
	+ compare last timestamp of 'Running' firing to current time
	+ notify on power resume, klexting (kiln text message)

Hardware:
- 20x4 LCD w/ i2c backpack
	+ $13, (https://www.amazon.com/gp/product/B01GPUMP9C/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1) uses RPLCD library
- MAX31856 thermocouple module
	+ $17.50, Adafruit (https://www.adafruit.com/product/3263);
    + not yet using, but want to switch soon, it is a much better chip than the MAX31855
- MAX31855 thermocouple module
	+ $14.95, Adafruit (https://www.adafruit.com/product/269);
- High temperature (2372 F) type K thermocouple
	+ $7/each, 3 pack, (https://www.aliexpress.com/item/High-Temperature-K-Type-Thermocouple-Sensor-for-Ceramic-Kiln-Furnace-1300-Temperature/32832729663.html?spm=a2g0s.9042311.0.0.3dd14c4dIQr1ud);
- Thermocouple wire:
    + I bought the 24awg yellow k-type stuff at the pottery store, amazon has it too;
    + I use about 8 feet, the controller is attached to the wall.
- 1 - uln2803a darlington transitor array to switch 12V coil on the relays
	+ $1/each on amazon, using 3 of 8 channels;
- 3 - Deltrol 20852-81 relays
	+ This is equivelent to relay Skutt uses to switch sections/zones (Skutt model is SPDT, this is same series but DPDT),
	+ $17.50 each and about that much for shipping (https://www.galco.com/buy/Deltrol-Controls/20852-81);
- 12V power supply
	+ converts 120vac to 12vdc;
	+ supplies 12v to relay coils, HDMI monitor, and 5v buck converter;
	+ $20 (https://www.amazon.com/gp/product/B00DECZ7WC/ref=oh_aui_detailpage_o01_s01?ie=UTF8&psc=1);
	+ rail mounted.
- 5V buck converter
	+ converts 12v to 5v USB connector for Pi power;
	+ $7 (https://www.amazon.com/gp/product/B071FJVRCT/ref=oh_aui_detailpage_o03_s00?ie=UTF8&psc=1);
- monitor w/HDMI input, mine is 1366x780;
- terminal blocks to distribute L1, L2, N and GND
	+ Ground, $6 (https://www.amazon.com/gp/product/B000K2MA9M/ref=oh_aui_detailpage_o05_s00?ie=UTF8&psc=1)
	+ L1,L2,Neutral, 3 @ $7/each, (https://www.amazon.com/gp/product/B000OTJ89Q/ref=oh_aui_detailpage_o05_s00?ie=UTF8&psc=1);
- #12 awg hi-temp appliance wire to each element;
- 3 ceramic 2 pole terminal blocks.
- crimp terminals, #10 awg, hi-temp appliance
	+ $.16/each, (https://www.amazon.com/gp/product/B01L2TL63C/ref=oh_aui_detailpage_o02_s00?ie=UTF8&psc=1);
	+ uses the same crimper used on the elements $16, (https://www.amazon.com/gp/product/B01L2TL63C/ref=oh_aui_detailpage_o02_s00?ie=UTF8&psc=1);
	+ the crimpers require muscle
- lugs #6 AWG copper
	+ $9 for 10 (https://www.amazon.com/gp/product/B073Y8Q9JQ/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1)
- big crimper
	+ $25, (https://www.amazon.com/gp/product/B07D7Q54N2/ref=oh_aui_detailpage_o01_s03?ie=UTF8&psc=1)
	+ I crimp 2 times, first time with correct size, second time reduced one notch(correct size is loose);
- din rail mounts
	+ $17/5 pair(https://www.amazon.com/gp/product/B01H1H86UU/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1);
- din rails
	+ $5/each (https://www.amazon.com/gp/product/B01FT485S0/ref=oh_aui_detailpage_o02_s01?ie=UTF8&psc=1);
- 14 THHN stranded, hardware store, to power 12V supply, white,red,greem 2' each
- heat shrink, Harbor Freight
- #10 32tpi tap and #21 jobber drill bit
	+ I have lots of 10-32 screws from rack mount hardware extras;
	+ drill and tap a hole, screw in a screw and use the $10 Harbor Freight angle grinder to cut it flush on the back of the box.

Thermocouple tip: One side of the type-K thermocouple and type-k wire is magnetic(red side), Test with magnet to wire correctly.


- Current kiln controller is attached to is a Old Skutt 281, which is a previous model number of KS1027:
  + old elements, I am surprised that it easily reaches temp at high speed, this kiln sat unused, outside under roof for 15 years, I don't want to put my new elements in it;
  + lid(split and flaking)repaired/coated;
  + base(cracks) repaired;
  + rust removal on controller boxes, painted;
  + built 2 steel rolling stands;


Stuff to get it to work:

- Pin-Out:

		RPLCD:		GPIO 2 SDA
		RPLCD:		GPIO 3 SCL
		RPLCD:		5V
		RPLCD:		GND
		MAX31855+:		3.3v
		MAX31855-:		GND
		MAX31855 CS:		GPIO 16
		MAX31855 DO:		GPIO 19
		MAX31855 CLK:		GPIO 21
		unl2003a 1:		GPIO 22 
		unl2003a 3:		GPIO 23
		unl2003a 5:		GPIO 24
		unl2003a 8:		GND
		unl2003a 9:		12V
		unl2003a 16:	relay #1 coil - (input is accross the chip on pin1)
		unl2003a 14:	relay #2 coil - (input is pin3)
		unl2003a 12:	relay #3 coil - (input is pin5)
        12V:	relay 1,2 and 3 coils

- Install PiLN files in /home and create log directory:

		sudo adduser PiLN
		su - PiLN
		git clone git@github.com:BlakeCLewis/MyPiLN.git .
		mkdir ./log

- Install sqlite3:

		sudo apt-get install sqlite3

- Set up directories/link for web page:

		sudo mkdir /var/www/html/images
		sudo mkdir /var/www/html/style
		chown pi:pi /var/www/html/style /var/www/html/images
		cp /home/PiLN/images/hdrback.png /var/www/html/images/hdrback.png
		cp /home/PiLN/images/piln.png   /var/www/html/images/piln.png
		cp /home/PiLN/style/style.css   /var/www/html/style/style.css

- !!!!!!! needs update to switched out Apache for lighttpd !!!
- Add the following ScriptAlias and Directory parameters under "IfDefine ENABLE_USR_LIB_CGI_BIN" in /etc/apache2/conf-available/serve-cgi-bin.conf:

		ScriptAlias /pilnapp/ /home/PiLN/app/
		<Directory "/home/PiLN/app/">
			AllowOverride None
			Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
			Require all granted
		</Directory>

- Create links to enable cgi modules:

		cd /etc/apache2/mods-enabled
		sudo ln -s ../mods-available/cgid.conf cgid.conf
		sudo ln -s ../mods-available/cgid.load cgid.load
		sudo ln -s ../mods-available/cgi.load cgi.load

- Restart Apache:

		sudo systemctl daemon-reload
		sudo systemctl restart apache2

- Install required Python packages:

		sudo raspi-config #enable interfaces ic2 & spi
		lsmod | grep spi

- Instal RPLCD for the 20x4 lcd:
		sudo pip install RPLCD
		sudo apt install python-smbus

- Install Adafruit MAX31855 Module:

		cd ~
		git clone https://github.com/adafruit/Adafruit_Python_MAX31855.git
		cd Adafruit_Python_MAX31855
		sudo python setup.py install

- create the sqlite3 database:

		sudo mkdir -p /var/www/db/PiLN/
		sudo chown -R PiLN:PiLN /var/www/db
		sqlite3 /var/www/db/PiLN/PiLN.sqlite3
		sqlite> .read /home/PiLN/PiLN.sql;

- Tuning: 

	+ Skutt KS1027 with old elements, minimal oscillation w/ very little overshoot:

            Kc               6.0
			Proportional:    5.0
			Integral:        1.0
			Derivative:     25.0
			Time internal:  30 seconds

- Using the Web App:

		On the same network that the RPi is connected, http://<RPi_IPAddress>/pilnapp/home.cgi
		Or, on the controler RPi, http://localhost/pilnapp/home.cgi

- Start the firing daemon:

		python3 ./daemon/pilnfired.py

- Glaze firing on March 3, 2019:

![:::](./PiLN_Firing-03-009-2019.png)

Test firing, I roasted some raw materials:

![:::](./mypiln_934C.png)

- Devices left to right/top to bottom:

		White wire goes to Kilnsitter;
		12V power supply from main AC voltage;
		4xUSB power jacks, steps 12v down to 5V;
		3 thermocouple chips, using 1, Thermocouple not yet hooked up;
		Raspbery Pi 3b with expermental board on top/with chip to drive 12v relays;
		3 relays, 1 for each kiln section;
		250 receptical, no control for manual kiln, maybe put it on big relay in futer;
		bus bars L1,L2,Neutral are covered, ground is bare;
		3 #12-2 w/ gnd power cords to kiln, 15' #6-3 w/8 gnd to RV receptical on back of garage. 
![:::](./mypiln_inside.png)

- This is the state of the kiln during the above 1000C test:
3 porcelain teminal blocks, with appliance high temp wire, each block feeds 1 section/2 elements.
![:::](./kiln_element_wiring.png)

- PID with C algorithm:

      This is a work in progress and I have not finish testing these instructions;
      My implementation of a PID algorithm that is optimaized for a system that can only add heat;

      Short comings:

          As presented, a change in window size will affect the P,I,D constants;
          I am working on a version scales with window size to reduce the affect of changing window size;
          C is not determined by a time sensitive value;
          P,I & D are determined by an amount of error over a time segment
              these terms should be normilazed by the time segment like (term*60/window)
      
      error = Setpoint - Currrent_temp;
      Pterm = Kp * error;
      Iterm = Summation (Ki * error), constrained by (Imin <= Iterm <= Imax);
      Dterm = Kd (error - previous_error);
      Cterm = Kc * (Current_temp - room_temp)/100;
      Window = determinied by bump test.

      Window:
          size of the base time unit, the controller will decide what to every window;
          is determined by kiln response time (how long it takes to finish reacting to input);
          window = 30;
          bump test

              turning on kiln for 30 seconds
              record temp/time every 10 seconds
              tau_temp = .75(hi_temp - start-temp)
              window = 1/4 (time at tau+temp)

      Cterm:

          Kc = 6;
          Steady state term, required amount of energy to maintain temp;
          it is linear, inverse proportional to r-value of kiln;
          this is my solution to the oscillating I could not tune out of PID;
          it probably is not an original thought;
          my kiln requires about 6% of output per 100C of temp differential;
          (100C ~= 6% to hold temp, 1000C ~= 60% to hold temp);
          tune:
              after determining "window", do a test run to 500C, with 10 minute holds every 100C;
              query the database to find the average output during the holds;
              mine was about 6% per 100C.

      Pterm:

          Kp = 5;
          An amount proportional to desired change in temp;
          this was an intuitive gues that worked

      Iterm:

          Ki = 1;
          Imin = -25;
          Imax = 25;
          Accumlitive error, corrects for past errors in (Cterm + Pterm);
          I look at it as incremental change in output to correct for error of (Cterm + Pterm);
          To reduce iIterm "Windup", Iterm is limited by (Imin <= Iterm <+ Imax).

      Dterm:

          Kd = 25;
          rate of change in error, d;
          Dterm needs to beable to cancel Item, another intuitive guess.

      Output:

          output = (Cterm + Pterm + Iterm + Dterm);
          output is a percentage and therefore constrained by (0 <= output <= 100)
          

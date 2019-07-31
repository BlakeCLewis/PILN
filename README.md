Electricity and heat are dangerous! Evaluate the risk and make go no go decision!

Web-based Raspberry Pi Kiln Control:
- achieved my goal to run on Rasberry Pi Zero W, but I am currently running on a Raspberry Pi 3b: 
	+ sqlite3 database for firing profiles and logging (very small memory footprint)
	+ lighttpd web server (very small memory footprint)

- kiln sitter(KS) as a sensor
	+ KS functions as 'ARMED', can not start firing without kilnsitter being armed
	+ set profile top temp higher than KS cone, KS is intended trigger, thermocouple is safety

Future improvements:
- performance watchdog:
	+ warning notifications, klexting;
	+ shutdown when a minimum rate cannot be maintained,
- inductive current sensors: element fault indication;
- crash/loss of power recovery:
	+ PI comes up, KS is armed & profile is 'Running' then how to consider unfinished segment
	+ compare temp at the timestamp to current temp
	+ compare last timestamp of 'Running' firing to current time
	+ notify on power resume, klexting (kiln text message)

Hardware:
- 20x4 LCD w/ i2c backpack
	+ $13, (https://www.amazon.com/gp/product/B01GPUMP9C/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1) uses RPLCD library
- 2 MAX31856 thermocouple module
	+ $17.50 each, Adafruit (https://www.adafruit.com/product/3263);
- High temperature (2372 F) type K thermocouple
	+ $7/each, 3 pack, (https://www.aliexpress.com/item/High-Temperature-K-Type-Thermocouple-Sensor-for-Ceramic-Kiln-Furnace-1300-Temperature/32832729663.html?spm=a2g0s.9042311.0.0.3dd14c4dIQr1ud);
- Thermocouple wire:
    + I bought the 24awg yellow k-type wire at the pottery store, amazon has it too;
    + I use about 6 feet, the controller is attached to the wall.
- 1 - uln2803a darlington transitor array to switch 12V fan and 12V coils of the relays
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
- 14 THHN stranded, hardware store, to power 12V supply, white,red,greem 2' each
- heat shrink, Harbor Freight

Thermocouple tip: One side of the type-K thermocouple and type-k wire is magnetic(red side), Test with magnet to wire correctly.

- Current kiln controller is attached to is a Old Skutt 281, which is a previous model number of KS1027:
  + old elements, I am surprised that it easily reaches temp at a reasonable rate, this kiln sat unused, outside under roof for 15 years;
  + lid(split and flaking)repaired/coated;
  + base(cracks) repaired;
  + rust removal on controller boxes, painted;
  + built rolling stand out of 2"x3" mild steel rectangular tube;


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
		unl2003a 7:             GPIO 13
		unl2003a 8:		GND
		unl2003a 9:		12V
		unl2003a 10:            FAN black/gnd
		unl2003a 16:	relay #1 coil (input is accross the chip on pin1)
		unl2003a 14:	relay #2 coil (input is pin3)
		unl2003a 12:	relay #3 coil (input is pin5)
        12V:	relay 1,2,3 coils and FAN red/+

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

- Install Adafruit MAX31856 Module:

		cd ~
		git clone https://github.com/adafruit/Adafruit_Python_MAX31856.git
		cd Adafruit_Python_MAX31856
		sudo python setup.py install

- create the sqlite3 database:

		sudo mkdir -p /var/www/db/PiLN/
		sudo chown -R PiLN:PiLN /var/www/db
		sqlite3 /var/www/db/PiLN/PiLN.sqlite3
		sqlite> .read /home/PiLN/PiLN.sql;

- Tuning: 

	+ Skutt KS1027 with old elements:
	
			Kc:   6.0% 
			Kp:   3.0
			Ki:   0.4
			Kd:  13.0
			Time internal:  30 seconds

- Using the Web App:

		On the same network that the RPi is connected, http://<RPi_IPAddress>/pilnapp/home.cgi
		Or, on the controler RPi, http://localhost/pilnapp/home.cgi

- Start the firing daemon:

		python3 ./daemon/pilnfired.py

- PID with C algorithm:

      This is a work in progress and I have not finish testing these instructions;
      My implementation of a PID algorithm that is optimaized for a system that can only add heat;

      Kc is not determined by a time sensitive value;
      Ki is not time sensitive;
      Kp & Kd are determined by an amount of error over a time segment 
          these terms should be normilazed by the time segment like (term*60/window)
      
      error = Setpoint - Currrent_temp;
      Pterm = Kp * 60/Window * error;
      Iterm = Summation (Ki * error), constrained by (Imin <= Iterm <= Imax);
      Dterm = Kd * 60/Window * (error - previous_error);
      Cterm = Kc/100 * (Current_temp - room_temp);
      Window = determinied by bump test, mine is 30 seconds

      Window:
          size of the base time unit, the controller will decide what to every window;
          determined by kiln response time (how long it takes to finish reacting to input);
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
          my kiln requires about 6% of output per 100C of temp differential;
          (100C ~= 6% to hold temp, 1000C ~= 60% to hold temp);
          tune:
              after determining "window", do a test run to 500C, with 10 minute holds every 100C;
              query the database to find the average output during the holds;
              mine was about 6% per 100C.

      Pterm:

          Kp = 3;
          Proportional to desired change in temp;
	  TODO - test runs with rate 60 and 166 C/hr, query the database and average(pid_output-Pterm) for each 100C segment.

      Iterm:

          Ki = 0.4;
          Imin = -25;
          Imax = 25;
          Accumlitive error, corrects for past errors in (Cterm + Pterm);
          I look at it as incremental change in output to correct for error of (Cterm + Pterm);
          To reduce Iterm "Windup", Iterm is limited by (Imin <= Iterm <+ Imax).

      Dterm:

          Kd = 13;
          rate of change in error;
          Dterm needs to be able to cancel the sum of the other 3 terms to slow/speed change in temp to keep from over shooting.

      Output:

          output = (Cterm + Pterm + Iterm + Dterm);
          output is a percentage and therefore constrained by (0 <= output <= 100)
          

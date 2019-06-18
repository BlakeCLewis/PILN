- C_PID algorithm: (Celcius)

      error = Setpoint - Currrent_temp;
      Cterm = Kc * (Current_temp - room_temp)/100;
      Pterm = Kp * error * 60/Window;
      Iterm = Summation (Ki * error), constrained by (Imin <= Iterm <= Imax);
      Dterm = Kd (error - last_error) * 60/Window;
      Window = in seconds, determinied by bump test.

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
          

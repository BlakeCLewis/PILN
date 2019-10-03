--   PiLN: Rassberry Pi electric kiln controller
--
--   Copyright (C) 2017  pvarney     git@github.com:pvarney/PiLN.git
--   Copyright (C) 2018  BlakeCLewis git@github.com:BlakeCLewis/PILN.git
--
--   This program is free software: you can redistribute it and/or modify
--   it under the terms of the GNU General Public License version 3
--   published by the Free Software Foundation.
--
--   This program is distributed in the hope that it will be useful,
--   but WITHOUT ANY WARRANTY; without even the implied warranty of
--   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
--   GNU General Public License for more details.
--
--   You should have received a copy of the GNU General Public License
--   along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
select printf('$%.2f',round(sum(pid_output)/2/60/60*12*.10,2)) from firing where run_id>44;


--kiln rated kwh = 12
--$/kwh = $0.11
-- 1/(100*60*60)=1/36000
select printf('$%.2f',round(sum(f.pid_output*s.int_sec)*12/360000*.11,2))
  from firing f,
       segments s
  where f.run_id>44
    and s.run_id=f.run_id
    and s.segment=f.segment;

select printf('$%.2f',round(sum(f.pid_output*s.int_sec)*kwh/100/60/60*.$/kwh,2)) 


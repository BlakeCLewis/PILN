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

CREATE TABLE IF NOT EXISTS profiles(
  run_id  INTEGER PRIMARY KEY,
  state   TEXT NOT NULL DEFAULT 'Staged',
  notes   TEXT,
  p_param REAL NOT NULL,
  i_param REAL NOT NULL,
  d_param REAL NOT NULL,
  start_time DATETIME DEFAULT NULL,
  end_time   DATETIME DEFAULT NULL
);
CREATE TABLE IF NOT EXISTS firing(
  run_id     INT NOT NULL,
  segment    INT NOT NULL DEFAULT 0,
  dt         DATETIME NOT NULL DEFAULT CURRENT_DATETIME,
  set_temp   NUMERIC NOT NULL,
  temp       NUMERIC NOT NULL,
  int_temp   NUMERIC DEFAULT NULL,
  pid_output NUMERIC NOT NULL,
  PRIMARY KEY(run_id,segment,dt)
);
CREATE TABLE IF NOT EXISTS segments(
  run_id   INT NOT NULL,
  segment  INT NOT NULL,
  set_temp INT NOT NULL,
  rate     INT NOT NULL,
  hold_min INT NOT NULL,
  int_sec  INT NOT NULL,
  start_time DATETIME DEFAULT NULL,
  end_time   DATETIME DEFAULT NULL,
  PRIMARY KEY (run_id,segment),
  FOREIGN KEY(run_id) REFERENCES profiles(run_id)
);

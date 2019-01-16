Lattice matching workflows and scripts

Make sure to export the `PROJ_fe_graph` environment variable to be able to run
the workflow contained within 00_run_all_jobs

BUMP | RF | 190116

# Instructions:
* Move entirety of `00_run_all_jobs` into a job folder
* Run `00_job_setup.py`
  * This will set up the directories
* Run '00_submit_manage_jobs.py'
  * This will submit the jobs

Dependencies:
* A lot of the code that's contained within my `PythonModules` repo

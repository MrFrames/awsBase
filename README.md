# Where-is-ben
Website which receives location data from gps tracker (android), stores to a mysql database & serves the latest location to users as a google map pin. To be developed into a site for tracking & displaying data for Farah, and her friends, as she is cycling from London to Iran later in the year.

Todo:

Phase 1, show route.
<ul> 
  <li> Make storage of data more secure.
  <li> Make map show previous route traveled.
</ul>

Phase 2, get stats.
<ul> 
  <li> Make secure login form/page for user.
  <li> user console: App analyses data & displays stats for user.
</ul>

Phase 3, join me
<ul> 
  <li> Make form for user to add key locations along route where people can meet up with them. 
  <li> App gathers data on predicted times to get to these locations.
  <li> Add toggle to main page to show meetup locations and info.
</ul>
Phase 4, analyse route
<ul> 
  <li> Add functionality to user console where user inputs the a difficulty rating due to various factors at end of day.
  <li> Use google API to get vectors and elevation at each datapoint, to calculate caloric load estimate for sections of route.
  <li> Use user input to predict which days are going to be difficult, and how many calories the user should be consuming.
</ul>

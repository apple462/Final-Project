### API DOCUMENTATION

# API-1
Methods: GET, POST
Endpoint: /tracker
Desc: Get/Post trackers}

# API-2
Methods: GET, PUT, DELETE
Endpoint: /tracker/<int: tracker_id>
Desc: Get/Update/Delete tracker by id

# API-3
Methods: GET, POST
Endpoint: /tracker/<int: tracker_id>/log
Desc: Get/Post logs in a tracker

# API-4
Methods: GET, PUT, DELETE
Endpoint: /tacker/<int: tracker_id>/log/<int: log_id>
Dec: Get/Update/Delete a log in a tracker by id

# API-5
Methods: GET
Endpoints: /tracker/<int: tracker_id>/logs/<int: period>
Desc: Get logs in a tracker in a period
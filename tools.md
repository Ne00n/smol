You can browse the web via shell:
python browse.py '<json>'

# Go to a page
python browse.py '{"action":"navigate","url":"news.ycombinator.com"}'

# Click the 3rd interactive element from the last response
python browse.py '{"action":"click","index":3}'

# Type into the 5th input field
python browse.py '{"action":"type","index":5,"text":"hello"}'

# Scroll down
python browse.py '{"action":"scroll","direction":"down"}'
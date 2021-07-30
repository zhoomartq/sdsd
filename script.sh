#!/bin/bash
echo 'Sleeping...'
sleep 5
echo 'Making /upload_form request'
curl -i --request POST 'localhost:8000/upload_form?name=qwerty&user_phone=phone&test=text'
echo

sleep 2
echo 'Making /get_form request'
curl -i --request POST 'localhost:8000/get_form?user_phone=8%20(456)%20789-56-43&test=123&vxxxx=123'
echo

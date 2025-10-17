#!/bin/bash

API_BASE="http://127.0.0.1:8000/v1/people"

create_person() {
    local first_name=$1
    local last_name=$2
    local mother_id=$3
    local father_id=$4
    
    curl -X 'POST' \
      "$API_BASE" \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d "{
        \"first_name\": \"$first_name\",
        \"last_name\": \"$last_name\",
        \"mother_id\": $mother_id,
        \"father_id\": $father_id
      }" 2>/dev/null
}

create_person "Иван" "Петров" "null" "null"
create_person "Мария" "Петрова" "null" "null"
create_person "Сергей" "Иванов" "null" "null"
create_person "Ольга" "Иванова" "null" "null"
create_person "Алексей" "Петров" "1" "2"
create_person "Елена" "Иванова" "3" "4"
create_person "Дмитрий" "Петров" "5" "6"
create_person "Анна" "Петрова" "5" "6"

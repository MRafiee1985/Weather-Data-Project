{{ config(
    materialized='table',
    unique_key='id'
) }}

with 
  source as (
    select *
    from {{ source('dev', 'raw_weather_data') }}
  ),                     
  de_dup as (
    select
      *,
      row_number() over (
        partition by time_local
        order by id desc
      ) as rn
    from source
  )                      

select                    
  id,
  city,
  temperature,
  weather_descriptions,
  wind_speed,
  time_local as weather_time_local
from de_dup                
where rn = 1
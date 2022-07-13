-- This model is defined here:
--   tests/functional/example/fixtures.py
select *
from {{ ref('my_model' )}}
where id is null

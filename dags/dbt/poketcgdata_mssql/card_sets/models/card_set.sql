{{
    config(
        materialized='incremental',
        unique_key='id'
    )
}}

select
    scs.id as id,
    scs.set_name as set_name,
    scs.total as total,
    scs.series as series,
    scs.printed_total as printed_total,
    scs.release_date as release_date,
    scs.api_updated_datetime as api_updated_datetime,
    scs.logo_img_url as logo_img_url,
    scs.symbol_img_url as symbol_img_url,
     case
        when scs.id not in (
            select id
            from cards.card_set
        ) then getdate()
        else (
            select cs.created_datetime
            from cards.card_set cs
            where scs.id = cs.id
        )
    end as created_datetime,
    case
        when scs.id in (
            select id
            from cards.card_set
        ) then getdate()
        else NULL
    end as updated_datetime
from {{ ref('stg_card_set') }} scs
    {% if is_incremental() %}
    where scs.id not in (
    	select id
    	from cards.card_set cs
    )
	or cast(api_updated_datetime as date) > (
        select cast(api_updated_datetime as date)
        from cards.card_set cs
        where scs.id = cs.id
    )
    {% endif %}
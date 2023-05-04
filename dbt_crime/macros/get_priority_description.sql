{# This macro returns the description of the priority for San Diego data #}

{% macro get_priority_description(priority) %}

    case {{ priority }}
        when 0 then 'Dispatch Immediately'
        when 1 then 'Dispatch Immediately'
        when 2 then 'Dispatch as quickly as possible'
        when 3 then 'Dispatch as quickly as possible'
        when 4 then 'Dispatch when no higher priority calls are waiting'
        when 9 then 'Calls that are formatted for the Telephone Report Unit'
    end

{% endmacro %}
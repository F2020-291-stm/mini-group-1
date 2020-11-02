select p.pid as pid, p.pdate as pdate, p.title as title, p.body as body, p.poster as poster, p.nov as nov, count(a.pid) as ano 
from(select p.pid as pid, p.pdate as pdate, p.title as title, p.body as body, p.poster as poster, count(v.pid) as nov, p.filter as filter
    from(
        <placeholder>) p
    left join votes v on p.pid = v.pid
    group by p.pid, p.pdate, p.title, p.body, p.poster, p.filter
    order by p.filter) p
left join answers a on a.qid = p.pid
group by p.pid, p.pdate, p.title, p.body, p.poster, p.nov
order by p.filter;
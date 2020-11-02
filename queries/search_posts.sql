select p.pid as pid, p.pdate as pdate, p.title as title, p.body as body, p.poster as poster, p.nov as nov, count(q.pid) as qno, count(a.pid) as ano 
from(select p.pid as pid, p.pdate as pdate, p.title as title, p.body as body, p.poster as poster, count(v.pid) as nov
    from(
        <placeholder>) s,
    posts p
    left join votes v on p.pid = v.pid
    where p.pid = s.pid
    group by p.pid, p.pdate, p.title, p.body, p.poster) p
left join questions q on p.pid = q.pid 
left join answers a on a.qid = p.pid
group by p.pid, p.pdate, p.title, p.body, p.poster, p.nov;
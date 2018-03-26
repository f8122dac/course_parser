import pickle
import sys

DEPT = sys.argv[-1] or 'amath' 
prereq_template = '{{||listPrereqTemplate}}'

get_filename = lambda x: fmt_title(x)[7:]+'.tid'
fmt_title    = lambda x: "title: {id}".format(**x)
fmt_tags     = lambda x: "tags: " + \
                           " ".join((
                               "[[course info]]", 
                               "[[lvl{0}]]".format(x['id'].strip()[-3]),
                               "[[{0}]]".format(x['id'][:-3].strip())
                           ))
fmt_credit   = lambda x: 'credit: ' + x['credit']
fmt_req      = lambda x: "" if 'req'     not in x.keys() else "genreq: {req}".format(**x)
fmt_prereq   = lambda x: "prereq: "+ ("none" if 'prereq'  not in x.keys() else " ".join("[[{}]]".format(t) for t in x['prereq']))
fmt_jointly  = lambda x: "" if 'jointly' not in x.keys() else "jointly: " + " ".join("[[{}]]".format(t) for t in x['jointly'])
fmt_text     = lambda x: "\n!!{id} {title} ({credit})\n{description}".format(**x) + "\n\n" \
                         + prereq_template
fmt_type     = lambda x: "type: text/vnd.tiddlywiki"

fmt_course_name = lambda x: "course_name: {title}".format(**x)

fmts         = ( fmt_title, 
                 fmt_tags, 
                 fmt_course_name,
                 fmt_credit, 
                 fmt_req,
                 fmt_prereq, 
                 fmt_jointly, 
                 fmt_type,
                 fmt_text     )

fmt_tid      = lambda x: {
                   'content' : "\n".join(filter(bool, map( lambda fmt: fmt(x), fmts ))),
                   'filename': get_filename(x) 
               }

data = pickle.load(open('out/p/{}.p'.format(DEPT), 'rb'))
dept = data[0]['id'][:-3].strip()
for t in map( fmt_tid, data):
    with open('out/tiddlers/'+t['filename'], 'w') as f:
        f.write(t['content'])

with open('out/tiddlers/{}.tid'.format(dept), 'w') as f:
    f.write("title: {}\ntags: [[Course Catalog]]\n".format(dept))


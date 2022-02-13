from lib.db.models.job_info import JobInfo, WAITING, EXECUTING
from lib.jinja_templates import get_template
from sanic.response import html, redirect


async def jobs(request):
    jobs = await JobInfo.all()
    job_infos = []
    for job in jobs:
        job_infos.append({
            'name': job.name,
            'info': job.info,
            'status': job.status,
            'error': job.error,
            'output': job.output
        })

    template = await get_template('jobs.html', request)
    return html(template.render(job_infos=job_infos))


async def jobs_post(request):
    if request.form.get('clear_jobs', None) is not None:
        await JobInfo.delete_where({'$and': [{
            'status': {
                '$ne': WAITING
            }
        }, {
            'status': {
                '$ne': EXECUTING
            }
        }]})
    return redirect('/jobs')

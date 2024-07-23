import subprocess

myrun = lambda cmd: subprocess.run(cmd,shell=True,text=True,capture_output=True)

build_commit_id = myrun('git rev-parse HEAD').stdout.strip()
print('commit id: ' + build_commit_id)

exist_remote_tags = myrun("git ls-remote --tags origin | awk '{print $2}'").stdout.splitlines()

r = myrun('git --no-pager tag')
for tag in r.stdout.splitlines():
    if 'rc' in tag or 'beta' in tag or 'build' in tag:
        continue
    if tag.startswith('0.') or tag.startswith('1.'):
        continue
    print(tag)
    if tag in exist_remote_tags:
        continue
    myrun(f'git reset --hard {tag}')
    myrun(f'git cherry-pick {build_commit_id}')
    myrun(f'git rm .github/workflows/ci.yml')
    myrun(f'git rm .github/workflows/codeql-analysis.yml')
    myrun(f"git commit -m 'fix: remove upstream ci'")
    myrun(f'git tag {tag}_buildtag')
    myrun(f'git push origin tag {tag}_buildtag')

myrun(f'git checkout main')

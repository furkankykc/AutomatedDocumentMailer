import datetime

from github import Github
def getGitRepo():
    g = Github("12bf9f12d5d0d500ad7f691c1ffced13f75e2e94")
    return g.get_user().get_repo('EmailAccounts')


def updateFile(file, commitMessage, content):
    try:
        sha = getGitRepo().get_file_contents(file).sha
        getGitRepo().update_file(file, commitMessage+str(datetime.datetime.now().microsecond),
                                 content,
                                 sha)

    except Exception as e:
        print(e)
        getGitRepo().create_file(file,
                                 commitMessage,
                                 content
                                 )




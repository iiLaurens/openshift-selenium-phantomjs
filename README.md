# openshift-selenium-phantomjs
This is a working example of using Selenium for Python (2.7) in combination with PhantomJS (1.9.8) on Openshift Online.

In order for this to work, PhantomJS had to be patched. The patch is included and automatically downloaded to the data folder during the deployment process. Note that the download process uses a openshift action_hook. For this to work, the action_hooks files need to be defined executable. If cloning on windows, please make sure you keep the action hooks executable using `git update-index --chmod=+x .openshift/action_hooks/*`.

Selenium is included locally in this repository as it needed adjustments for the patched version of PhantomJS to work.

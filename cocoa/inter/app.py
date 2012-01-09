import logging

from jobprogress import job
import cocoa
from cocoa import install_exception_hook, proxy
from cocoa.inter import signature, subproxy, PyFairware
from hscommon.trans import trget

from core.app import JobType
from .result_table import PyResultTable
from .stats_label import PyStatsLabel

tr = trget('ui')

JOBID2TITLE = {
    JobType.Scan: tr("Scanning for duplicates"),
    JobType.Load: tr("Loading"),
    JobType.Move: tr("Moving"),
    JobType.Copy: tr("Copying"),
    JobType.Delete: tr("Sending to Trash"),
}

class PyDupeGuruBase(PyFairware):
    def _init(self, modelclass):
        logging.basicConfig(level=logging.WARNING, format='%(levelname)s %(message)s')
        install_exception_hook()
        appdata = proxy.getAppdataPath()
        self.py = modelclass(self, appdata)
        self.progress = cocoa.ThreadedJobPerformer()
    
    def bindCocoa_(self, cocoa):
        self.cocoa = cocoa
    
    resultTable = subproxy('resultTable', 'result_table', PyResultTable)
    statsLabel = subproxy('statsLabel', 'stats_label', PyStatsLabel)
    
    #---Directories
    def addDirectory_(self, directory):
        return self.py.add_directory(directory)
    
    #---Results
    def clearIgnoreList(self):
        self.py.scanner.ignore_list.Clear()
    
    def doScan(self):
        self.py.start_scanning()
    
    def exportToXHTML(self):
        return self.py.export_to_xhtml()
    
    def loadSession(self):
        self.py.load()
    
    def loadResultsFrom_(self, filename):
        self.py.load_from(filename)
    
    def markAll(self):
        self.py.mark_all()
    
    def markNone(self):
        self.py.mark_none()
    
    def markInvert(self):
        self.py.mark_invert()
    
    def purgeIgnoreList(self):
        self.py.purge_ignore_list()
    
    def toggleSelectedMark(self):
        self.py.toggle_selected_mark_state()
    
    def saveSession(self):
        self.py.save()
    
    def saveResultsAs_(self, filename):
        self.py.save_as(filename)
    
    #---Actions
    def addSelectedToIgnoreList(self):
        self.py.add_selected_to_ignore_list()
    
    def deleteMarked(self):
        self.py.delete_marked()
    
    def hardlinkMarked(self):
        self.py.delete_marked(replace_with_hardlinks=True)
    
    def applyFilter_(self, filter):
        self.py.apply_filter(filter)
    
    def makeSelectedReference(self):
        self.py.make_selected_reference()
    
    def copyOrMove_markedTo_recreatePath_(self, copy, destination, recreate_path):
        self.py.copy_or_move_marked(copy, destination, recreate_path)
    
    def openSelected(self):
        self.py.open_selected()
    
    def removeMarked(self):
        self.py.remove_marked()
    
    def renameSelected_(self,newname):
        return self.py.rename_selected(newname)
    
    def revealSelected(self):
        self.py.reveal_selected()
    
    def invokeCommand_(self, cmd):
        self.py.invoke_command(cmd)
    
    #---Information
    def getIgnoreListCount(self):
        return len(self.py.scanner.ignore_list)
    
    def getMarkCount(self):
        return self.py.results.mark_count
    
    @signature('i@:')
    def scanWasProblematic(self):
        return bool(self.py.results.problems)
    
    @signature('i@:')
    def resultsAreModified(self):
        return self.py.results.is_modified
    
    #---Properties
    @signature('v@:c')
    def setMixFileKind_(self, mix_file_kind):
        self.py.scanner.mix_file_kind = mix_file_kind
    
    @signature('v@:c')
    def setEscapeFilterRegexp_(self, escape_filter_regexp):
        self.py.options['escape_filter_regexp'] = escape_filter_regexp
    
    @signature('v@:c')
    def setRemoveEmptyFolders_(self, remove_empty_folders):
        self.py.options['clean_empty_dirs'] = remove_empty_folders
    
    @signature('v@:c')
    def setIgnoreHardlinkMatches_(self, ignore_hardlink_matches):
        self.py.options['ignore_hardlink_matches'] = ignore_hardlink_matches
    
    #---Worker
    def getJobProgress(self):
        try:
            return self.progress.last_progress
        except AttributeError:
            # I have *no idea* why this can possible happen (last_progress is always set by
            # create_job() *before* any threaded job notification, which shows the progress panel,
            # is sent), but it happens anyway, so there we go. ref: #106
            return -1
    
    def getJobDesc(self):
        try:
            return self.progress.last_desc
        except AttributeError:
            # see getJobProgress
            return ''
    
    def cancelJob(self):
        self.progress.job_cancelled = True
    
    def jobCompleted_(self, jobid):
        self.py._job_completed(jobid)
    
    #--- model --> view
    def open_path(self, path):
        proxy.openPath_(str(path))
    
    def reveal_path(self, path):
        proxy.revealPath_(str(path))
    
    def start_job(self, jobid, func, args=()):
        try:
            j = self.progress.create_job()
            args = tuple([j] + list(args))
            self.progress.run_threaded(func, args=args)
        except job.JobInProgressError:
            proxy.postNotification_userInfo_('JobInProgress', None)
        else:
            ud = {'desc': JOBID2TITLE[jobid], 'jobid':jobid}
            proxy.postNotification_userInfo_('JobStarted', ud)
    
    def show_extra_fairware_reminder(self):
        self.cocoa.showExtraFairwareReminder()
    
    def show_message(self, msg):
        self.cocoa.showMessage_(msg)
    

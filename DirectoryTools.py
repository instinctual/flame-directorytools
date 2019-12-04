# DirectoryTools for Flame v1.0
# Original Copyright (c) 2019 Bob Maple (bobm-matchbox [at] idolum.com)
# Modified by Gary Oberbrunner, garyo@darkstarsystems.com, for Instinctual
#
# For Flame 2020 and above - place in /opt/Autodesk/shared/python/
#
# Adds a submenu to the MediaHub context menu in Files mode to tar and zip
# a selected directory or directories (makes separate files for each)
#
# Select a directory in the browser and right-click to access
#
# Uses Backburner to run tar commands


import os, subprocess, time, tempfile, shlex

config = dict(
  BBMANAGER="manager",
  BBGROUP="TARNODES",
  PRIORITY="30",
  CMDJOB="/opt/Autodesk/backburner/cmdjob"
)

def ask_yesno(dlg_msg, dlg_title):
  """Prompt user for yes/cancel using Qt widgets"""
  from PySide2.QtWidgets import QMessageBox

  qtMsgBox = QMessageBox()
  qtMsgBox.setWindowTitle( dlg_title )
  qtMsgBox.setText( dlg_msg )
  qtMsgBox.setStandardButtons( QMessageBox.Yes | QMessageBox.Cancel )
  qtMsgBox.setDefaultButton( QMessageBox.Yes )
  res = qtMsgBox.exec_()

  if res == QMessageBox.Cancel :
  	return( False )
  else:
  	return( True )

#


##### Main Flame hook handler
#####

def get_mediahub_files_custom_ui_actions():

  def menu_enabled(sel) :
    if os.path.isdir( sel[0].path ) :
      return True
    else :
      return False

  def tardir_go(sel, prompt=ask_yesno, test_mode=False) :
    if not prompt('{} folder(s) selected for TAR; OK?'.format(len(sel)),
                  'tarring {} folder(s)'.format(len(sel))):
      return

    for curitem in sel:
      if not os.path.isdir(curitem.path):
        continue
      archive_path = curitem.path + '.tar'
      if os.path.isfile(archive_path) and \
         not prompt( "Overwrite " + archive_path + " ?", archive_path + " exists" ):
        continue

      # Run on Backburner using cmdjob
      vars = config.copy()
      vars['TARDIR'] = curitem.path
      vars['BASENAME'] = os.path.basename(curitem.path)
      vars['JOBNAME'] = os.path.basename(curitem.path) + ' DCDM'
      vars['PARENTDIR'] = os.path.dirname(curitem.path)

      cmdline = ['{CMDJOB}',
                 '-manager:{BBMANAGER}',
                 '-group:{BBGROUP}',
                 '-priority:{PRIORITY}',
                 '-jobName', '{JOBNAME}',
                 '-userRights',
                 '-description', 'TAR + List file',
                 'sh', '-c',
                 '/usr/bin/tar -cvf {TARDIR}.tar -C {PARENTDIR} {BASENAME} ; '
                 ' tar -tvf {TARDIR}.tar | sort > {TARDIR}.tar.list']
      cmdline = [x.format(**vars) for x in cmdline]

      if test_mode:
        return cmdline

      # Run job
      cmd = subprocess.Popen(cmdline)
      rc = cmd.wait()
      return rc

  return [
    {
      "name": "Directory Tools",
      "actions": [
        {
          "name": "TAR Directory",
          "isEnabled": menu_enabled,
          "execute": tardir_go
        },
      ]
    }
  ]

# Use pytest to run this test
def test_tar(monkeypatch):
  """Test the tar action -- check resulting cmd line and try a dummy run"""
  class PathItem:
      def __init__(self, path):
        self.path = path

  def fake_askyesno(msg, title):
    return True

  for d in ('/tmp/foo', '/tmp/foo/bar'):
    try:
      os.mkdir(d)
    except OSError:
      pass

  actions = get_mediahub_files_custom_ui_actions()
  sel = [PathItem('/tmp/foo')]
  tardir_go = actions[0]['actions'][0]['execute']
  cmdline = tardir_go(sel, fake_askyesno, True)
  assert cmdline[0] == config['CMDJOB']
  assert '/usr/bin/tar -cvf /tmp/foo.tar -C /tmp foo ;  tar -tvf /tmp/foo.tar | sort > /tmp/foo.tar.list' in cmdline

  # Now actually try it
  rc = tardir_go(sel, fake_askyesno, False)
  assert rc in (0, 6)           # 0 = success, 6 = connection refused

  # Clean up
  for d in ('/tmp/foo/bar', '/tmp/foo'):
    try:
      os.rmdir(d)
    except OSError:
      pass

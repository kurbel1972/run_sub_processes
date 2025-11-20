import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import os
import time
import subprocess

class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'MyServiceRunSubProcessesNew'
    _svc_display_name_ = 'My Service Run Sub Processes New'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(120)
        self.is_alive = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = False
        servicemanager.LogInfoMsg(f"{self._svc_name_} is stopping.")

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
        servicemanager.LogInfoMsg(f"{self._svc_name_} has started.")
        self.main()

    def main(self):
        # Caminho para o script Python que será executado
        script_path = r'C:\Pessoal\Trabalho\GIT\run_sub_processes\run_sub_processes.py'
        
        # Loop principal do serviço
        while self.is_alive:
            try:
                # Usar subprocess para rodar o script Python
                servicemanager.LogInfoMsg(f"Attempting to run script: {script_path}")
                subprocess.run(['python', script_path], check=True)
                servicemanager.LogInfoMsg(f"Script {script_path} completed successfully.")
            except subprocess.CalledProcessError as e:
                servicemanager.LogErrorMsg(f"Error running script {script_path}: {e}")
            except Exception as e:
                servicemanager.LogErrorMsg(f"Unexpected error while running script {script_path}: {e}")
            
            # Aguardar 15 minutos (900 segundos) antes de executar novamente
            servicemanager.LogInfoMsg(f"Waiting for 15 minutes before running script {script_path} again.")
            time.sleep(900)

    @classmethod
    def set_service_start_type(cls):
        # Conectar ao gerenciador de serviços
        service_manager = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)
        # Abrir o serviço para alterar a configuração
        service_handle = win32service.OpenService(service_manager, cls._svc_name_, win32service.SERVICE_CHANGE_CONFIG)
        # Alterar o tipo de inicialização para Automático
        win32service.ChangeServiceConfig(
            service_handle,
            win32service.SERVICE_NO_CHANGE,    # Tipo de serviço (sem alteração)
            win32service.SERVICE_AUTO_START,   # Tipo de inicialização (Automático)
            win32service.SERVICE_NO_CHANGE,    # Tipo de erro (sem alteração)
            None,  # Caminho do executável (None se não mudar)
            None,  # Grupo de carregamento (None se não mudar)
            0,     # Tag ID (0 se não usar tags)
            None,  # Dependências (None se não houver)
            None,  # Conta do serviço (None para manter a atual)
            None,  # Senha (None para manter a atual)
            None   # Nome de exibição (None para manter o nome atual)
        )
        # Fechar os handles do serviço e do gerenciador
        win32service.CloseServiceHandle(service_handle)
        win32service.CloseServiceHandle(service_manager)

if __name__ == '__main__':
    if len(os.sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MyService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        if 'install' in os.sys.argv:
            win32serviceutil.HandleCommandLine(MyService)
            MyService.set_service_start_type()  # Define o serviço como automático
        else:
            win32serviceutil.HandleCommandLine(MyService)

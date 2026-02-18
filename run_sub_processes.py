import subprocess
import sys
import re

def is_vpn_connected():
    try:
        result = subprocess.run(['route', 'print'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
        # print("Output from route print:", output)  # Debug: Prints the output of the route print command to check network routes
        
        # Checks if there is any route indicating the presence of the VPN
        if re.search(r'185\.2\.\d+\.\d+', output):
            print("Company VPN detected.")  # Debug: Confirmation that the VPN was detected
            return True
        else:
            print("Company VPN not detected.")  # Debug: Indicates that the VPN was not found in the output
            return False
    except Exception as e:
        print(f"Error checking VPN connection: {e}", file=sys.stderr)
        return False

def main():
    if is_vpn_connected():  # Commented - also works from office network
    # if True:  # Allow execution from VPN or office network
        print("VPN is connected.")
        try:
            # Execute your main script
            subprocess.run(['python', 'recupera_precon.py'], check=True)
            print("********************************* Script recupera_precon executed successfully. *********************************")
        except subprocess.CalledProcessError as e:
            print(f"Error executing the script: {e}", file=sys.stderr)
        try:
            # Execute your main script
            subprocess.run(['python', 'verifica_objetos_gidwin.py'], check=True)
            print("********************************* Script verifica_objetos_gidwin executed successfully. *********************************")
        except subprocess.CalledProcessError as e:
            print(f"Error executing the script verifica_objetos_gidwin: {e}", file=sys.stderr)
        #try:
        #    # Execute your main script
        #    subprocess.run(['python', 'trata_alfandega_excel_new.py'], check=True)
        #    print("********************************* Script trata_alfandega_excel_new executed successfully. *********************************")
        #except subprocess.CalledProcessError as e:
        #    print(f"Error executing the script trata_alfandega_excel_new: {e}", file=sys.stderr)
        try:
            # Execute your main script
            subprocess.run(['python', 'send_files_year_bk.py'], check=True)
            print("********************************* Script send_files_year_bk executed successfully. *********************************")
        except subprocess.CalledProcessError as e:
            print(f"Error executing the script send_files_year_bk: {e}", file=sys.stderr)
        try:
            # Execute your main script
            subprocess.run(['python', 'send_files_year_bk_items.py'], check=True)
            print("********************************* Script send_files_year_bk_items executed successfully. *********************************")
        except subprocess.CalledProcessError as e:
            print(f"Error executing the script send_files_year_bk_items: {e}", file=sys.stderr)
        try:
            # Execute your main script
            subprocess.run(['python', 'send_files_exportacao_bck.py'], check=True)
            print("********************************* Script send_files_year_bk executed successfully. *********************************")
        except subprocess.CalledProcessError as e:
            print(f"Error executing the script send_files_year_bk: {e}", file=sys.stderr)
        try:
            # Execute your main script
            subprocess.run(['python', 'send_edi_email_messages_new.py'], check=True)
            print("********************************* Script send_edi_email_messages_new executed successfully. *********************************")
        except subprocess.CalledProcessError as e:
            print(f"Error executing the script send_edi_email_messages_new: {e}", file=sys.stderr)
    else:
        print("VPN is not connected.")

if __name__ == "__main__":
    main()

def generar_email(nombre_usuario='', username='', password='', pagina='https://kipka.sistema-web.com/inicio/ingresar'):

    cuerpoEmail = f'''
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html dir="ltr" lang="es">
    <head>
        <link
        rel="preload"
        as="image"
        href="http://www.unipol.edu.bo/wp-content/uploads/2021/12/LOGO-IITCUP-768x768.jpg" />
        <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
        <meta name="x-apple-disable-message-reformatting" />
    </head>
    <body
        style='background-color:rgb(243,244,246);font-family:ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";padding-top:40px;padding-bottom:40px'>
        <!--$-->
        <div
        style="display:none;overflow:hidden;line-height:1px;opacity:0;max-height:0;max-width:0">
        Credenciales de acceso - Kipka
        </div>
        <table
        align="center"
        width="100%"
        border="0"
        cellpadding="0"
        cellspacing="0"
        role="presentation"
        style="background-color:rgb(255,255,255);max-width:600px;margin-left:auto;margin-right:auto;border-radius:8px;box-shadow:var(--tw-ring-offset-shadow, 0 0 #0000), var(--tw-ring-shadow, 0 0 #0000), 0 10px 15px -3px rgb(0,0,0,0.1), 0 4px 6px -4px rgb(0,0,0,0.1)">
        <tbody>
            <tr style="width:100%">
            <td>
                <table
                align="center"
                width="100%"
                border="0"
                cellpadding="0"
                cellspacing="0"
                role="presentation"
                style="background-color:rgb(30,58,138);color:rgb(255,255,255);text-align:center;padding-top:32px;padding-bottom:32px;border-top-left-radius:8px;border-top-right-radius:8px">
                <tbody>
                    <tr>
                    <td>
                        <img
                        alt="Logo Gubernamental"
                        src="http://www.unipol.edu.bo/wp-content/uploads/2021/12/LOGO-IITCUP-768x768.jpg"
                        style="width:80px;height:auto;object-fit:cover;margin-left:auto;margin-right:auto;margin-bottom:16px;display:block;outline:none;border:none;text-decoration:none" />
                        <h1 style="font-size:24px;font-weight:700;margin:0px;color:rgb(255,255,255)">
                        Instituto De Investigaciones Técnico Científicas De La Universidad Policial
                        </h1>
                        <p
                        style="font-size:14px;color:rgb(219,234,254);margin:0px;margin-top:0px;line-height:24px;margin-bottom:0px;margin-left:0px;margin-right:0px">
                        KIPKA
                        </p>
                    </td>
                    </tr>
                </tbody>
                </table>
                <table
                align="center"
                width="100%"
                border="0"
                cellpadding="0"
                cellspacing="0"
                role="presentation"
                style="padding-left:32px;padding-right:32px;padding-top:32px;padding-bottom:32px">
                <tbody>
                    <tr>
                    <td>
                        <h1
                        style="font-size:20px;font-weight:700;color:rgb(31,41,55);margin-bottom:16px">
                        Credenciales de Acceso al Sistema
                        </h1>
                        <p
                        style="font-size:16px;color:rgb(55,65,81);line-height:24px;margin-bottom:24px;margin-top:16px">
                        Estimado/a
                        <!-- -->{nombre_usuario}<!-- -->,
                        </p>
                        <p
                        style="font-size:16px;color:rgb(55,65,81);line-height:24px;margin-bottom:24px;margin-top:16px">
                        Se han generado sus credenciales de acceso al Sistema Kipka. Estas credenciales le permitirán
                        acceder a los servicios y funcionalidades asignadas según
                        su perfil de usuario.
                        </p>
                        <table
                        align="center"
                        width="100%"
                        border="0"
                        cellpadding="0"
                        cellspacing="0"
                        role="presentation"
                        style="background-color:rgb(249,250,251);border-width:1px;border-color:rgb(229,231,235);border-radius:8px;padding:24px;margin-bottom:24px">
                        <tbody>
                            <tr>
                            <td>
                                <table
                                align="center"
                                width="100%"
                                border="0"
                                cellpadding="0"
                                cellspacing="0"
                                role="presentation">
                                <tbody style="width:100%">
                                    <tr style="width:100%">
                                    <td data-id="__react-email-column">
                                        <p
                                        style="font-size:14px;font-weight:700;color:rgb(75,85,99);margin-bottom:0px;margin:0px;line-height:24px;margin-top:0px;margin-left:0px;margin-right:0px">
                                        NOMBRE DE USUARIO:
                                        </p>
                                        <p
                                        style='font-size:16px;font-family:ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;background-color:rgb(255,255,255);border-width:1px;border-color:rgb(209,213,219);border-radius:4px;padding:12px;margin:0px;margin-bottom:0px;line-height:24px;margin-top:0px;margin-left:0px;margin-right:0px'>
                                        {username}
                                        </p>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>
                                <table
                                align="center"
                                width="100%"
                                border="0"
                                cellpadding="0"
                                cellspacing="0"
                                role="presentation">
                                <tbody style="width:100%">
                                    <tr style="width:100%">
                                    <td data-id="__react-email-column">
                                        <p
                                        style="font-size:14px;font-weight:700;color:rgb(75,85,99);margin-bottom:0px;margin:0px;line-height:24px;margin-top:0px;margin-left:0px;margin-right:0px">
                                        CONTRASEÑA TEMPORAL:
                                        </p>
                                        <p
                                        style='font-size:16px;font-family:ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;background-color:rgb(255,255,255);border-width:1px;border-color:rgb(209,213,219);border-radius:4px;padding:12px;margin:0px;line-height:24px;margin-bottom:0px;margin-top:0px;margin-left:0px;margin-right:0px'>
                                        {password}
                                        </p>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>
                            </td>
                            </tr>
                        </tbody>
                        </table>
                        <table
                        align="center"
                        width="100%"
                        border="0"
                        cellpadding="0"
                        cellspacing="0"
                        role="presentation"
                        style="margin-bottom:24px">
                        <tbody>
                            <tr>
                            <td>
                                <h1
                                style="font-size:18px;font-weight:700;color:rgb(31,41,55);margin-bottom:16px">
                                Instrucciones de Acceso:
                                </h1>
                                <p
                                style="font-size:16px;color:rgb(55,65,81);line-height:24px;margin-bottom:12px;margin-top:16px">
                                1. Ingrese al portal oficial:
                                <a
                                    href="{pagina}"
                                    style="color:rgb(37,99,235);text-decoration-line:underline"
                                    target="_blank"
                                    >{pagina}</a
                                >
                                </p>
                                <p
                                style="font-size:16px;color:rgb(55,65,81);line-height:24px;margin-bottom:12px;margin-top:16px">
                                2. Utilice las credenciales proporcionadas arriba
                                </p>
                                <p
                                style="font-size:16px;color:rgb(55,65,81);line-height:24px;margin-bottom:12px;margin-top:16px">
                                3. Se le recomienda cambiar su contraseña en el
                                primer acceso
                                </p>
                                <p
                                style="font-size:16px;color:rgb(55,65,81);line-height:24px;margin-bottom:16px;margin-top:16px">
                                4. Configure sus datos de recuperación de cuenta
                                </p>
                            </td>
                            </tr>
                        </tbody>
                        </table>
                        <hr
                        style="border-color:rgb(209,213,219);margin-top:24px;margin-bottom:24px;width:100%;border:none;border-top:1px solid #eaeaea" />
                        <table
                        align="center"
                        width="100%"
                        border="0"
                        cellpadding="0"
                        cellspacing="0"
                        role="presentation"
                        style="background-color:rgb(254,242,242);border-left-width:4px;border-color:rgb(239,68,68);padding:20px;margin-bottom:24px">
                        <tbody>
                            <tr>
                            <td>
                                <h1
                                style="font-size:16px;font-weight:700;color:rgb(153,27,27);margin-bottom:12px;display:flex;align-items:center">
                                ⚠️ ADVERTENCIAS DE SEGURIDAD
                                </h1>
                                <p
                                style="font-size:14px;color:rgb(185,28,28);line-height:20px;margin-bottom:0px;margin:0px;margin-top:0px;margin-left:0px;margin-right:0px">
                                • NO comparta sus credenciales con terceros
                                </p>
                                <p
                                style="font-size:14px;color:rgb(185,28,28);line-height:20px;margin-bottom:0px;margin:0px;margin-top:0px;margin-left:0px;margin-right:0px">
                                • NO responda a este correo electrónico
                                </p>
                                <p
                                style="font-size:14px;color:rgb(185,28,28);line-height:20px;margin-bottom:0px;margin:0px;margin-top:0px;margin-left:0px;margin-right:0px">
                                • Cambie su contraseña inmediatamente después del
                                primer acceso
                                </p>
                                <p
                                style="font-size:14px;color:rgb(185,28,28);line-height:20px;margin-bottom:0px;margin:0px;margin-top:0px;margin-left:0px;margin-right:0px">
                                • Cierre sesión al finalizar cada uso del sistema
                                </p>
                                <p
                                style="font-size:14px;color:rgb(185,28,28);line-height:20px;margin:0px;margin-bottom:0px;margin-top:0px;margin-left:0px;margin-right:0px">
                                • Reporte cualquier actividad sospechosa
                                inmediatamente
                                </p>
                            </td>
                            </tr>
                        </tbody>
                        </table>
                        <table
                        align="center"
                        width="100%"
                        border="0"
                        cellpadding="0"
                        cellspacing="0"
                        role="presentation"
                        style="background-color:rgb(239,246,255);border-width:1px;border-color:rgb(191,219,254);border-radius:8px;padding:20px;margin-bottom:24px">
                        <tbody>
                            <tr>
                            <td>
                                <h1
                                style="font-size:16px;font-weight:700;color:rgb(30,64,175);margin-bottom:12px">
                                Información Adicional:
                                </h1>
                                <p
                                style="font-size:14px;color:rgb(29,78,216);line-height:20px;margin-bottom:0px;margin:0px;margin-top:0px;margin-left:0px;margin-right:0px">
                                • Horario de atención: Lunes a Viernes, 8:00 -
                                18:00
                                </p>
                                <p
                                style="font-size:14px;color:rgb(29,78,216);line-height:20px;margin-bottom:0px;margin:0px;margin-top:0px;margin-left:0px;margin-right:0px">
                                • Las credenciales expiran en
                                <!-- -->30<!-- -->
                                días si no se utilizan
                                </p>
                                <p
                                style="font-size:14px;color:rgb(29,78,216);line-height:20px;margin:0px;margin-bottom:0px;margin-top:0px;margin-left:0px;margin-right:0px">
                                • Este mensaje es generado automáticamente
                                </p>
                            </td>
                            </tr>
                        </tbody>
                        </table>
                        <p
                        style="font-size:16px;color:rgb(55,65,81);line-height:24px;margin-bottom:16px;margin-top:16px">
                        Atentamente,<br />Kipka<br />Instituto De Investigaciones Técnico Científicas De La Universidad Policial
                        </p>
                    </td>
                    </tr>
                </tbody>
                </table>
                <table
                align="center"
                width="100%"
                border="0"
                cellpadding="0"
                cellspacing="0"
                role="presentation"
                style="background-color:rgb(31,41,55);color:rgb(255,255,255);padding-left:32px;padding-right:32px;padding-top:24px;padding-bottom:24px;border-bottom-right-radius:8px;border-bottom-left-radius:8px">
                <tbody>
                    <tr>
                    <td>
                        <p
                        style="font-size:12px;color:rgb(209,213,219);text-align:center;line-height:18px;margin:0px;margin-bottom:0px;margin-top:0px;margin-left:0px;margin-right:0px">
                        Este es un mensaje automático del sistema. No responda a
                        este correo.
                        </p>
                        <p
                        style="font-size:12px;color:rgb(209,213,219);text-align:center;line-height:18px;margin:0px;margin-bottom:0px;margin-top:0px;margin-left:0px;margin-right:0px">
                        Av. Abel Iturralde, entre las calles Haití y Guatemala, N° 1122, Zona Miraflores - La Paz Bolivia
                        </p>
                        <p
                        style="font-size:12px;color:rgb(209,213,219);text-align:center;line-height:18px;margin:0px;margin-bottom:0px;margin-top:0px;margin-left:0px;margin-right:0px">
                        ©
                        <!-- -->2025<!-- -->
                        <!-- -->IITCUP<!-- -->. Todos los
                        derechos reservados.
                        </p>
                    </td>
                    </tr>
                </tbody>
                </table>
            </td>
            </tr>
        </tbody>
        </table>
        <!--7--><!--/$-->
    </body>
    </html>
    '''
    return cuerpoEmail

def generar_email_codigo(codigo_verificacion='', pagina='https://kipka.sistema-web.com/inicio/ingresar'):

    cuerpoEmail = f'''
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html dir="ltr" lang="es">
    <head>
        <link
        rel="preload"
        as="image"
        href="http://www.unipol.edu.bo/wp-content/uploads/2021/12/LOGO-IITCUP-768x768.jpg" />
        <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
        <meta name="x-apple-disable-message-reformatting" />
    </head>
    <body
        style='background-color:rgb(243,244,246);font-family:ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";padding-top:40px;padding-bottom:40px'>
        <!--$-->
        <div
        style="display:none;overflow:hidden;line-height:1px;opacity:0;max-height:0;max-width:0">
        Credenciales de acceso - Kipka
        </div>
        <table
        align="center"
        width="100%"
        border="0"
        cellpadding="0"
        cellspacing="0"
        role="presentation"
        style="background-color:rgb(255,255,255);max-width:600px;margin-left:auto;margin-right:auto;border-radius:8px;box-shadow:var(--tw-ring-offset-shadow, 0 0 #0000), var(--tw-ring-shadow, 0 0 #0000), 0 10px 15px -3px rgb(0,0,0,0.1), 0 4px 6px -4px rgb(0,0,0,0.1)">
        <tbody>
            <tr style="width:100%">
            <td>
                <table
                align="center"
                width="100%"
                border="0"
                cellpadding="0"
                cellspacing="0"
                role="presentation"
                style="background-color:rgb(30,58,138);color:rgb(255,255,255);text-align:center;padding-top:32px;padding-bottom:32px;border-top-left-radius:8px;border-top-right-radius:8px">
                <tbody>
                    <tr>
                    <td>
                        <img
                        alt="Logo Gubernamental"
                        src="http://www.unipol.edu.bo/wp-content/uploads/2021/12/LOGO-IITCUP-768x768.jpg"
                        style="width:80px;height:auto;object-fit:cover;margin-left:auto;margin-right:auto;margin-bottom:16px;display:block;outline:none;border:none;text-decoration:none" />
                        <h1 style="font-size:24px;font-weight:700;margin:0px;color:rgb(255,255,255)">
                        Instituto De Investigaciones Técnico Científicas De La Universidad Policial
                        </h1>
                        <p
                        style="font-size:14px;color:rgb(219,234,254);margin:0px;margin-top:0px;line-height:24px;margin-bottom:0px;margin-left:0px;margin-right:0px">
                        KIPKA
                        </p>
                    </td>
                    </tr>
                </tbody>
                </table>
                <table
                align="center"
                width="100%"
                border="0"
                cellpadding="0"
                cellspacing="0"
                role="presentation"
                style="padding-left:32px;padding-right:32px;padding-top:32px;padding-bottom:32px">
                <tbody>
                    <tr>
                    <td>
                        <h1
                        style="font-size:20px;font-weight:700;color:rgb(31,41,55);margin-bottom:16px">
                        Credenciales de Acceso al Sistema
                        </h1>
                        <p
                        style="font-size:16px;color:rgb(55,65,81);line-height:24px;margin-bottom:24px;margin-top:16px">
                        Estimado Usuario
                        
                        </p>
                        <p
                        style="font-size:16px;color:rgb(55,65,81);line-height:24px;margin-bottom:24px;margin-top:16px">
                        Se han generado sus codigo de verificacion para el acceso al Sistema Kipka. Este codigo le permitirá
                        iniciar sesión
                        </p>
                        <table
                        align="center"
                        width="100%"
                        border="0"
                        cellpadding="0"
                        cellspacing="0"
                        role="presentation"
                        style="background-color:rgb(249,250,251);border-width:1px;border-color:rgb(229,231,235);border-radius:8px;padding:24px;margin-bottom:24px">
                        <tbody>
                            <tr>
                            <td>
                                <table
                                align="center"
                                width="100%"
                                border="0"
                                cellpadding="0"
                                cellspacing="0"
                                role="presentation">
                                <tbody style="width:100%">
                                    <tr style="width:100%">
                                    <td data-id="__react-email-column">
                                        <p
                                        style="font-size:14px;font-weight:700;color:rgb(75,85,99);margin-bottom:0px;margin:0px;line-height:24px;margin-top:0px;margin-left:0px;margin-right:0px">
                                        Codigo de Verificación:
                                        </p>
                                        <p
                                        style='font-size:16px;font-family:ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;background-color:rgb(255,255,255);border-width:1px;border-color:rgb(209,213,219);border-radius:4px;padding:12px;margin:0px;margin-bottom:0px;line-height:24px;margin-top:0px;margin-left:0px;margin-right:0px'>
                                        {codigo_verificacion}
                                        </p>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>
                            </td>
                            </tr>
                        </tbody>
                        <hr
                        style="border-color:rgb(209,213,219);margin-top:24px;margin-bottom:24px;width:100%;border:none;border-top:1px solid #eaeaea" />
                        <table
                        align="center"
                        width="100%"
                        border="0"
                        cellpadding="0"
                        cellspacing="0"
                        role="presentation"
                        style="background-color:rgb(254,242,242);border-left-width:4px;border-color:rgb(239,68,68);padding:20px;margin-bottom:24px">
                        <tbody>
                            <tr>
                            <td>
                                <h1
                                style="font-size:16px;font-weight:700;color:rgb(153,27,27);margin-bottom:12px;display:flex;align-items:center">
                                ⚠️ ADVERTENCIAS DE SEGURIDAD
                                </h1>
                                <p
                                style="font-size:14px;color:rgb(185,28,28);line-height:20px;margin-bottom:0px;margin:0px;margin-top:0px;margin-left:0px;margin-right:0px">
                                • NO comparta sus credenciales con terceros
                                </p>
                                <p
                                style="font-size:14px;color:rgb(185,28,28);line-height:20px;margin-bottom:0px;margin:0px;margin-top:0px;margin-left:0px;margin-right:0px">
                                • NO responda a este correo electrónico
                                </p>
                                <p
                                style="font-size:14px;color:rgb(185,28,28);line-height:20px;margin-bottom:0px;margin:0px;margin-top:0px;margin-left:0px;margin-right:0px">
                                • Cambie su contraseña inmediatamente después del
                                primer acceso
                                </p>
                                <p
                                style="font-size:14px;color:rgb(185,28,28);line-height:20px;margin-bottom:0px;margin:0px;margin-top:0px;margin-left:0px;margin-right:0px">
                                • Cierre sesión al finalizar cada uso del sistema
                                </p>
                                <p
                                style="font-size:14px;color:rgb(185,28,28);line-height:20px;margin:0px;margin-bottom:0px;margin-top:0px;margin-left:0px;margin-right:0px">
                                • Reporte cualquier actividad sospechosa
                                inmediatamente
                                </p>
                            </td>
                            </tr>
                        </tbody>
                        </table>
                        <table
                        align="center"
                        width="100%"
                        border="0"
                        cellpadding="0"
                        cellspacing="0"
                        role="presentation"
                        style="background-color:rgb(239,246,255);border-width:1px;border-color:rgb(191,219,254);border-radius:8px;padding:20px;margin-bottom:24px">
                        <tbody>
                            <tr>
                            <td>
                                <h1
                                style="font-size:16px;font-weight:700;color:rgb(30,64,175);margin-bottom:12px">
                                Información Adicional:
                                </h1>
                                <p
                                style="font-size:14px;color:rgb(29,78,216);line-height:20px;margin-bottom:0px;margin:0px;margin-top:0px;margin-left:0px;margin-right:0px">
                                • Horario de atención: Lunes a Viernes, 8:00 -
                                18:00
                                </p>
                                <p
                                style="font-size:14px;color:rgb(29,78,216);line-height:20px;margin-bottom:0px;margin:0px;margin-top:0px;margin-left:0px;margin-right:0px">
                                • Las credenciales expiran en
                                <!-- -->30<!-- -->
                                días si no se utilizan
                                </p>
                                <p
                                style="font-size:14px;color:rgb(29,78,216);line-height:20px;margin:0px;margin-bottom:0px;margin-top:0px;margin-left:0px;margin-right:0px">
                                • Este mensaje es generado automáticamente
                                </p>
                            </td>
                            </tr>
                        </tbody>
                        </table>
                        <p
                        style="font-size:16px;color:rgb(55,65,81);line-height:24px;margin-bottom:16px;margin-top:16px">
                        Atentamente,<br />Kipka<br />Instituto De Investigaciones Técnico Científicas De La Universidad Policial
                        </p>
                    </td>
                    </tr>
                </tbody>
                </table>
                <table
                align="center"
                width="100%"
                border="0"
                cellpadding="0"
                cellspacing="0"
                role="presentation"
                style="background-color:rgb(31,41,55);color:rgb(255,255,255);padding-left:32px;padding-right:32px;padding-top:24px;padding-bottom:24px;border-bottom-right-radius:8px;border-bottom-left-radius:8px">
                <tbody>
                    <tr>
                    <td>
                        <p
                        style="font-size:12px;color:rgb(209,213,219);text-align:center;line-height:18px;margin:0px;margin-bottom:0px;margin-top:0px;margin-left:0px;margin-right:0px">
                        Este es un mensaje automático del sistema. No responda a
                        este correo.
                        </p>
                        <p
                        style="font-size:12px;color:rgb(209,213,219);text-align:center;line-height:18px;margin:0px;margin-bottom:0px;margin-top:0px;margin-left:0px;margin-right:0px">
                        Av. Abel Iturralde, entre las calles Haití y Guatemala, N° 1122, Zona Miraflores - La Paz Bolivia
                        </p>
                        <p
                        style="font-size:12px;color:rgb(209,213,219);text-align:center;line-height:18px;margin:0px;margin-bottom:0px;margin-top:0px;margin-left:0px;margin-right:0px">
                        ©
                        <!-- -->2025<!-- -->
                        <!-- -->IITCUP<!-- -->. Todos los
                        derechos reservados.
                        </p>
                    </td>
                    </tr>
                </tbody>
                </table>
            </td>
            </tr>
        </tbody>
        </table>
        <!--7--><!--/$-->
    </body>
    </html>
    '''
    return cuerpoEmail
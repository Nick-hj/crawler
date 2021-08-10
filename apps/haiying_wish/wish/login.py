# -*- coding: utf-8 -*-
# @Time    : 2021/7/21 10:07
# @Author  : Haijun
import re
import execjs
import requests

# session = requests.Session()
# url = 'https://www.wish.com/api/email-login'
# data = {
#     'email': 'haijun0422@126.com',
#     'password': 'haijun308329',
#     'is_product_page': 'false',
#     'url': 'https://www.wish.com/',
#     'recaptcha_token': '03AGdBq25xIRtssSljedyTd32oy_DsvIFahE7DzZanOsEwwKUdaX_1ziG8ZnmQxh9KHnSvnyHTwnikc9-ti22L6ZQM4D844lt4VeD3LzU9YPuoEElgltsQeAs5tnVN-sOf4DuHZdG5pNvXQF4rm3IFhO2tc3uwpvf0B-qDkV-yGFD23BIY9uDrUEW7HdSlnQQU0yF_eFVurGzX96pOLE1sY7WJPeCAiub0iPeTXOPkCRJEnxI00juo8jWpAjP-qEafAQpZY-QSVc7cdK8EvfvHPDMuhkcLELCvD9XWDEVdmRAPCO8TLwB5XLFHXIqXJaaOFYNjDUFqm2Lts7jgcnzahco9kxSGKyVuBt63anzW63tFkqmXAOKGAjjPPdbUXMEmQKl_qv1g13PSygNiEB2o8E0VCKPyQGKRVaGuJn1L8CrxYw_rnfUV0UB4n5VXTfrFuRWh_AefK1Xx',
#     'securedtouch_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiYVkwVDRpLzN1MFUzcVZiMkllZVJDVEtuN0hrOGdjeHJlbEFheUdTRTB4djl0STN6MnVkaUpaWlFKT3ZyNjJ5cHBNU2JWY1IwZXdoSUl2N0grR2QyTUhmS05LL2pSMEIrdENZcVdaUjdVWVBOWEVBWjhnT0htc2RKdlBCSUpKRUxmWFQrcXB1WlNKeWUwU1FhdkNnTm5TZWZrM25QdW1VbWlVMTQvQ2RPQXlBSVA4ZFM4bDM4YjlVYjYvTjFtNGVOMVVlVnl5UitaVCtPUWhkMnpWc1NEZFpROS82T1FyeG1DYXI3eXlKaUNYbkZLbDNMWTZtSGg2M3ZmWWJ3YzZnNFpZakJOUG9VekdNVlpBbEJ2TkkxeEoyNlhsQ0FoTm9VV2RLQ1R1ZTlaYXVQWmZGb29FRWM4Wnhva1VyeW5JWkhlaHVtZjY3YnVzaHphVTdpRkJXdFB3SE9rc2pLZmR0SUhTZXhnWkg3V2FFPSIsImlhdCI6MTYyNjg1MDkyNiwiZXhwIjoxNjI4MDYwNTI2fQ.sVBZIDvhM7B2Rz8yvx_I7GY3Qk6whtqOelqDxD_ZO0E'
# }
# headers = {
#     'x-pc8g5v7m-a': 'MjPHrVj0a39YT_iinQAxfakquEpGKglPvZi-ZBFEADqJmf3gJJgaGOnsn12ORjQM_JF=o0xbRX=dmiMHuE57bZzUYtKcmG8uxUW9pEaa6qigT8=vLDr95KHIRc=vTMO4UB_c7CMbH4Ts=BNiVATxIoMDDO9wo8gls_9qfNYM4GitiKKbsm7AL-IHC3WYa_mr7gve79Qb-Q2nwCCZ72_LjzEGGblTcIxTy303B0HWUGiO4tqT=wqdTdwcJe3Vx9uH0WhXjMQ82gJjN=nJw4KeIp8PvRmI3yR64VU3Ax0PVKjhdqnRCD7gPZ8exNbj4VPAP2fD6vNjPE05JVEg87fPAGKWJzBwEPxc6P_ftlUV3bDy1tk7JXdHcNpB1-Z3JQ-TkHFd_9FNuykCl4VqEtVwZjfXgrbxHp4fLHEZ2HrXwLf=8pHux9BTPzzZii8KNr5mH=FddO73x8CLv1lZ15Xwu6bJm6o2GOv5YokYrN4Q3cCULoCXFPA8gJQ78m9JnnwOg9zxDNda1453XUk8wcDnPnZZ2bcrDT1_VI70arrLskbyhKxv2EJdOPRN-1r2hgNYQAWj-UeIGfw4wEhK82zzrjgGlNpFML5kfuhiUeFhRsoJ5k=n3TN6mO2K9W6svnK_L4n3woF7kQeq7Ux9RE6_h_6dkYZz_gzAA3sUo1w3QmKaEXTJTUI255jUPGfqr_2uj760CKDt=KwQk9rolI10CbyZPrcapoKY3Qfq7tIatPD1aY1dqJqgKQJ7lOXQ_ur_OgYT4RnLw6WlXRbh=54n5n8E6grVgf3sN4gUuxiveZ_xFQ10PR_7HVgyf30bisGiKLgmoj6HE=vOx0gHje9i87a8UufetGwE0sBZvg8VcZ1QpHA3fFK85vOCL_k=Y-sbxcvewFFPfKOmJ2sRoucBPWZyblk5H9Bbut32KF2-nHfW0E5OMv01X_2GXYcBjbQAhxRdqmWMN-Dw46bIFx2iIO0NUkNiaH03oxlnz1Pigm3lML4Bg==ykydI4VnuFiAgTEnf3RQbooPkI5_cbkIJ=3ATXzqOGZzi0uZRdd7rFKRoc8CdOHs7ERAQR7qI2RfRAuKgjuaK-1I8=YMPcJUrJsd8LqY1byLjQzYtdbvj8daHQGduYhJYkhfNDnEjrMLjPsIgL8GpNItYRH6QEvAEi-Y2wx0vp4m2E=lTTTOUgFp0NxFvKdhkOQfmq11i1MNLBVPzE4QiLfb9Q9UUGnjsvNWFEx=eQliD2c49kIZ6draaaVkK-9eW7pFbtQuAip-xBy3LUf56bBY_8XWl6mpqbtvsNXvNDeeTiXLZUcTsLXxU8hOEAdJaJ7jkgNsFvzLU2jOTLJbvmawW83Z7jeIhNY2TY5MPKoVKHfUbCAq0dpGtGfQW_jO2JvVRmwlm762XCK0xRXVq-noUixelNA=N05IXfBHMMcQ-eF2M6thvnzNsulj3AzOA7_CVNwbR55rxgHTs=Wb4RwgLWFfZT8DLRKKDmzk01wexmOPk_f6MO01NyNmXXTnXwKs9q20zmmOsEERntoqtC4dHCxQavyWeLtT-ARAPU8BU=wJWW3EtIW609yOF4THf_63Q49J2ICJa6XlR_rrtPsIbdl2gMh4kxX_HCwidvtpUz4ZMiCJidc-2t3R0oa_O_d61zno_Et4k5hJFuPoa2Mk6xLb71Z5XpcE=0kwxtlcfxGdZiJuoftinQT3syPxHRmvJX8co2KeoJBqe0Ww_ZpUkOwYGE0et0FFzFm1Mre08yW4sPcVwE1f5Jwq4HmHsKHC-czmEtRe9W6FVv8k3wYwAFjEUKFI4LUWLM3lVMkOmjiIk40QR2L4vWGZojXld_RD-fFbtUi9duk0xu7=k-WdlIYRJddMsl5brd4Ncsq4iqaAMUB77hEbldwWR-OhzGPLK7KfjpQzLWLTC9qULBbTp48gC-UQeTw7dqRuCRCeEP3G8--Xbu_-s=PZPAFqubPj_l8OBon38BricrcTW6Xb0jQbbVOV=2vmjVoGrZWTRf8JbtWvdTUQD4b=4KeLYwUuqjXwF-M4HoMZJg=85rcIpZo2vPgfHlEwoZ5pcLL=7as-x0__Y5Y2Vzsn8i1fhU_D3aFDV8JhIxHtDd6ZbAVwBh3GDcmxVdx=ege_Bty4VKnu-ZgUvL_IDd-5e9eB9KMmLsQxOyn-cDzgKCqtBdA36viL2kDnBDk69VLZVqPdnJMI=3zkr=DU-svH9yy-UMqRTOpZ_jWrZWNEIItma=BiYJGPbeDjL=KVTCDKipQBPAXHfOJBjQoDB2iCV_lDPOtIMkJ8wl7Pi6QK=81NQziIUw91HzPYhAMcDtfNzJrjBtlLvmA-svffdIxmnq1MV0uyzrU2Ggmr2I_0Y6Kc_DG-7759UUwH8k8CvbQhOAqM=s=_yPwZGpMPI9Rfk-DF44uaomogPJ=dUTROcUDoFJZ6WlT1RJfIVUNpvl4vFw-QZxn3QW=Wp0un610foWea91EDLgW9z_Fx3PVf7OOpkFfxTv67s8bZmM5_1DqXjIiOFwlEp2abbli_x_0oxQalZqR6kLpY=mCGIEd6iyyU=pK=6wB0JZtze2xB1L0RyCD43g9d-bghoysir25ChvrZFxDIjT8URaXj2KDkZW91A9z_=emxY6Qs4GyZm0cfHUUknUQeizDOgIrrnPzjhU7mFZ8hFqCoFY5Tp3o9EVUwKUCt30IIwi14eBZDjJFC6cI4ZQzzt5gd0RDvl2h7OLncJ3tn=28iDkzjtDi4=6sE97TO2F5RIBq07JFFgrYlcBbAai42x-ngLPiiy3w6i-z9Iv26ukbwYsRXBxcarVt=jTXz8MIOa6-nuREzGL7RLqtfO38zcEbhiETyKc=xMzqPFgDzDden8v637X8hi2UexBeEcE7qHA5On84cPW3KnbOcEKFmGtI8rqNzGLKXmJLr1bDf0sFEY4uUcGXiGc9-U-jJnUoTEv7pgMhxIe7xt17fHa8EWlAHoatJQChs2RlgKB6OA1sjlWfx2raMzW-ta9UDCN9hg4yjG5hCJ4IfJNQ-dfIkObRncxpck0oQNspyEL=H2xKD0RG5xfq-lIgkFkDG6UGq7ENDL87AMj0rmvoffNAdRz0QkX7jJXJ5J0V126azG0mhk6nXr9krZ2hWKofBWhRyF8ZGH0hWjzp22HuhZTA60DAlzzOyG1hafEEUsWD5BwGDrU38=kpn2lTjjxbnv94yr6X3phjtBF3ncmNW7x3MzWM2rqMJeeZPkocaG=KtljTm3z8CYczd7bNKG9qn3NX_ZKGi0W85W9Okqx1VOZhT7B1kCDdUGmw=e-RgtI-mule575jrqPc72jlyvonD8ZXEMzEtHEMBvimMHK5mxv7hyKFy9_x=8sdpv62JAFD7Cxx8m8ar5aPv4rMAWLnyIM-IFMqx-D4fjKPaYloc5Q5H2kj08l7lxWMootY0csvdWLJGvKfl1NXcluNsTfd4axv2FR-qBGavTXMx0IKg4dEG0-A2FaYNXToN98NAIkwRdQ0=IB=Uoen=q11DOr2RiDj5z0iivfPk2fnsG-px-AQ7Qhft5ADeascbV3Wncr6B1hjD1pIEP6z7ATYfyeQZ3DBaCRqz2A60xQzsALIE24Uvl4m5rkrjgB3lwG-xrJoETenl2VidExE8H-i7DcJu9P7tOdNYmR0ldROkO9DuzDzrAyLysobM00AeCiNFPRKniVlw60oJAF4saD7AXRinjvkP-5lTribHQ1ezOkNgI9eP6X4IiQK=wrgKyk=7tJcZOZhXt0=TyWdbo2E23J8xa1IHzbjxYk08T__-xGoPFnEJl63rtvXON=zs-YBobwtgrnZfiRfDO-vVxo77Vwf7RP_XwE4h87vtIAOccKYZe23RzstmF0ylTf0-Jcx6b33hvorHyaaWrN6z1cGmMXZ-oX_7pLWzl3b_8hTvp6gyoVP-7_=j50N4f_jIX0sdP4dgkLdN9OBxXIIYWMKIlZOpY82q6rNsbdV-P7KU=PCMlZGEr_4xry128jCQhTns61TApmYletKN3woXfCOnZFlTZogO4OQCGE3iZRR5bInYxJwq=6P6e=0_xqEfsvYXQ_dgn9dlLjPMhCUl9ZMaMsdQW2btJ2T5B-iXz_O-D42E66D1ho3rBVXgyrmlr4XP6PFGYDMBv1yvnIP0x4CLpZffep_pxJ7LHv4OT01CbPI9e-N92vt5jn56E9bw1C9WHV8G33vBmXu6yCCP9ocsR=uxqsgP=C0j4OhtkUmbcoMVAVGPmKLgEX9dcXVfQj0IaeZIEDIxvNc-0A4CdePvpmKBMG_hNsWT4B9gRHEwGcczZWWoQ-yA3FRfy=qImnus_60tK=9mRXswKHp2yXP6=TJLK1a0lyxesLWfVBGQBsBXJtMDBHcloUiCxbTKvrFFxGF0q9RH3w3aROv-YwVOnJFROxp2X559zp7h_8W1V9bqyuRPGqKHDEbEm1FUiYJiRolXXjqZxiANjBaJkemjb9rDc2gjyzGQprToiq_AyOajde8zPeeq66VY26At_fN5bHtfEEmEfe7ELD3peBTRxJPObEa4VjwfPnnVX7Kj2-r5jRDZuzIi2bP4WHN4hrMi6cINk-4NC8nqWLe5kAIjQPWNNyYumO2ZWvXlU3Yz=pI_LBMsEBGPsRzHDBTp4A3Lx-mxUprYH87ITrcI8=qOW85lh29sbvILjdHUsomvVkVd91-aWX9n0hjxdRrqXApLtzA7e1fo5ZklFB4hZWOyKgXrH4C3v-hrVCyQ-HrUTlUbmxXOBiy=elGrbG06itD4ntpUlRW2p13-M2afdDfzFKjxvLzFrkqjQxiLwMp1vvlHwsgGmMNpGsU8A5hXFRzyXR8lm4IZOsCD2M5xZvL_CXpnLLJR_Oald_-Z89-wzaugbkcABuqQCw_eu0QMghqg5igEho84iJo90liL=GyGjk3sCCIBaAs0MXX3=r2Xn0p-R4u8s3ZZ4UPlayihpb18NGH4gOeBW0Ln9IsgPBXubMqbqaB6-8ENht2eLdAkcuH5P7iFHTLc2Ps-T9sYx=F_67ZiaXn2cBmnNuda19EQ6mVzoJoU',
#     'x-pc8g5v7m-b': '-fswsu6',
#     'x-pc8g5v7m-c': 'AIAx3cd6AQAA43AE3O8BeD2GfZnNVkDzEKwggG96fUAkH0U7Xdo8nv7pSrsE',
#     'x-pc8g5v7m-d': 'ABaChIjBDKGNgUGAQZIQhISi0eIApJmBDgDaPJ7-6Uq7BAAAAABCiXEEACD-dUfmRNyjxrz7yveu2tg',
#     'x-pc8g5v7m-f': 'AwjC3sd6AQAAopQMYt6Or0xcc955G4xqQjAh95IEleBrw506-0vvlzfUN35aAS_wOyCucg00wH8AAEB3AAAAAA==',
#     'accept': 'application/json, text/plain, */*',
#     'content-type': 'application/x-www-form-urlencoded',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
#     'x-xsrftoken': '2|427466df|68e325514b44a19832bc225c658ae800|1626850921',
#     'cookie': 'visitor_id=19a53d15a09b4096ad4d4f0469ce13a7; __ssid=556b8d5b45f1d1c2b700f30258fb2a6; __stripe_mid=88ee989b-8933-40e9-8cd5-66a1f908317b8f7ed2; _pin_unauth=dWlkPU1EUTFOVE16T1dVdE5UZ3dZaTAwWmprNExXSmlOamN0TmpGbE1qRTJOV0l6TjJZMw; G_ENABLED_IDPS=google; _fbp=fb.1.1626252903523.1770009377; authentication_id=d6101e62950b3588a45b497b0e43279a; _dcmn_p=x6VeY2lkPXVXSFBNMkR6MU1QeF95RjJBQk0; _dcmn_p=x6VeY2lkPXVXSFBNMkR6MU1QeF95RjJBQk0; rskxRunCookie=0; rCookie=f0aeiu1l57m1c5q9wiutw3kr8yw9ke; _ga=GA1.2.1279326244.1626252829; _ga_S8FFZTJ4RL=GS1.1.1626628281.2.0.1626628281.0; tatari-session-cookie=e5934199-0a0d-39d6-9727-d192537bc499; _gid=GA1.2.941870162.1626774351; IR_gbd=wish.com; IR_PI=807ae331-3513-11eb-99e3-42010a246309%7C1626937305563; lastRskxRun=1626850913696; __stripe_sid=f9460fa1-23ec-4e5f-8362-e679aeb1070b80b3cf; logged_out_tracker=00fd48871fbba43da3596fb7f5525c1e7d38e26d90b52bb45aa95b9d2f28ffb3; logged_out_locale=en; bsid=112c0ad7815840d19e7486dc56ac1afe; _xsrf=2|427466df|68e325514b44a19832bc225c658ae800|1626850921; _timezone=8; _is_desktop=true; sweeper_uuid=3b9c788dd6fb49fc9c66ac107feaee23; _uetsid=0750ed20e79611eb97ea616a5c45d489; _uetvid=02c9c510e48111ebbd9e89268d36dcf9; IR_12396=1626850925816%7C0%7C1626850925816%7C%7C'
# }
# res = session.post(url=url, headers=headers, data=data)
# print(res.status_code)
# print(res.text)
# g_headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
# }
# g_url = f'https://www.wish.com/product/605daa4e1db8eb8ab8046b1a?share=web'
# response = session.get(url=g_url, headers=g_headers)
# _data_str = re.search(r'window.__PRELOADED_STATE__ = (.*?)</script>', response.text, re.S)
# # print(_data_str.group(1))
node = execjs.get()
ctx = node.compile(open('./xx.js',encoding='utf-8').read())
func = 'getPwd("{0}","{1}")'.format(1,2)
ctx.evel()
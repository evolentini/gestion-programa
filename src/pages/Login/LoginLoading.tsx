import React, { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import queryString from "query-string";
import axios from "axios";
import Cookies from 'js-cookie';
import useAuth from "../../hooks/useAuth";
import { BASE_URL } from '../../helpers/env-variables'

const LoginLoading: React.FC = () => {
  const {setAuth} = useAuth()
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const values = queryString.parse(location.search);
    const code = values.code ? values.code : null;

    if (code) {
      onGooglelogin();
    }
  }, []);

  const googleLoginHandler = (code: string) => {
    return axios
      .get(`${BASE_URL}auth/login/google/${code}`)
      .then((res) => {
        const { user, access_token, refresh_token } = res.data;
  
        setAuth({
          isLoggedIn: true,
          userEmail: user.email,
          userFirstName: user.first_name,
          userLastName: user.last_name,
        });

        const horaActual = new Date();
        const quinceMinutosDespues = new Date(horaActual.getTime() + 15 * 60 * 1000);
        const sieteDiasDespues = new Date(horaActual.getTime() + 7 * 24 * 60 * 60 * 1000);

        Cookies.set('token', access_token, { expires: quinceMinutosDespues, secure: true });
        Cookies.set('refresh_token', refresh_token, { expires: sieteDiasDespues, secure: true });

        navigate('/')
        return res.data;
      })
      .catch((err) => {
        return err;
      });
  };

  const onGooglelogin = async () => {
    await googleLoginHandler(location.search);
  }

  return <div>Just a moment</div>
}

export default LoginLoading

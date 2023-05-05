module.exports = {
    apps : [{
       name: 'sweetcakeserv',
       script: 'manage.py',
       args: 'runserver 0.0.0.0:8000 --insecure',
       interpreter: 'python3',
    }]
  }
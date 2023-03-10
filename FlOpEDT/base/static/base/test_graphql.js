query = "query { modules (dept : \"INFO\") { edges { node { name } } } }" 
$.ajax({
    type: "GET",
    // dataType: 'text',
    // headers: {Accept: 'text/csv'},
    url: url_graphql,
    async: true,
    success: function (msg, ts, req) {
      console.log(msg)
    },
    error: function (msg, ts, req) {
      console.log("error");
      console.log(req)
      console.log(ts)
    },
    contentType: 'application/json',
    data: JSON.stringify({"query": query}),
  });
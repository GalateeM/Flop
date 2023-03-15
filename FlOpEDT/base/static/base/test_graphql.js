const query = `
  query {
    modules (dept :\"INFO\", week : "{\\"week\\" : 13, \\"year\\" : 2022}"){
      edges {
        node {
          name,
          abbrev
          url
        }
      }
    }
  }
`;
console.log(query)
$.ajax({
  type: "GET",
  url: url_graphql,
  data: { query: query },
  success: function(response) {
    console.log(response);
  },
  error: function(error) {
    console.log(error);
  }
});
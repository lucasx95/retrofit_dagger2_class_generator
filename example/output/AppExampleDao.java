package exp.data;

public class AppExampleDao implements ExampleDao {

	private final ExampleService exampleService;

	@Inject
	public AppExampleDao(@NonNull final ExampleService exampleService) {
		this.exampleService = exampleService;
	}

	@Override
	public Example createExample(final ExampleDto exampleDto) throws GeneralDaoErrorException {
		try {
			Response<Example> response = exampleService
				.createExample(exampleDto).execute();
			if (response.code() != ResponseConstants.OK) throw new GeneralDaoErrorException(GeneralErrorCode.GENERIC);
			return response.body();
		} catch (Exception exception) {
			throw new GeneralDaoErrorException(exception.getMessage());
		}
	}

	@Override
	public List<Example> getAllExamplesFiltered(final Long testId, final String begin, final String end, final String status) throws GeneralDaoErrorException {
		try {
			Response<List<Example>> response = exampleService
				.getAllExamplesFiltered(testId, begin, end, status).execute();
			if (response.code() != ResponseConstants.OK) throw new GeneralDaoErrorException(GeneralErrorCode.GENERIC);
			return response.body();
		} catch (Exception exception) {
			throw new GeneralDaoErrorException(exception.getMessage());
		}
	}

	@Override
	public Void testExample(final ExampleDto exampleDto) throws GeneralDaoErrorException {
		try {
			Response<Void> response = exampleService
				.testExample(exampleDto).execute();
			if (response.code() != ResponseConstants.OK) throw new GeneralDaoErrorException(GeneralErrorCode.GENERIC);
			return response.body();
		} catch (Exception exception) {
			throw new GeneralDaoErrorException(exception.getMessage());
		}
	}

}